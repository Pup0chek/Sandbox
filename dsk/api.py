from typing import Optional, Dict, Any, Generator, Literal
import json
import cloudscraper


from .pow import DeepSeekPOW

ThinkingMode = Literal['detailed', 'simple', 'disabled']
SearchMode = Literal['enabled', 'disabled']


class DeepSeekError(Exception):
    """Base exception for all DeepSeek API errors"""
    pass


class AuthenticationError(DeepSeekError):
    """Raised when authentication fails"""
    pass


class RateLimitError(DeepSeekError):
    """Raised when API rate limit is exceeded"""
    pass


class NetworkError(DeepSeekError):
    """Raised when network communication fails"""
    pass


class APIError(DeepSeekError):
    """Raised when API returns an error response"""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class DeepSeekAPI:
    BASE_URL = "https://chat.deepseek.com/api/v0"

    def __init__(self, auth_token: str):
        if not auth_token or not isinstance(auth_token, str):
            raise AuthenticationError("Invalid auth token provided")
        self.auth_token = auth_token
        self.pow_solver = DeepSeekPOW()

        # Создаём scraper с подробным профилем браузера и длительной задержкой
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True},
            delay=60  # Задержка в 60 секунд (можно попробовать уменьшить, если 60 слишком много)
        )

        # Первый запрос для получения начальных cookies (например, __cf_bm, __cf_clearance и т.п.)
        try:
            initial_resp = self.scraper.get("https://chat.deepseek.com", timeout=10)
            print("Initial cookies:", self.scraper.cookies)
        except Exception as e:
            print("Ошибка при первичном запросе для получения cookies:", e)

        # Дополнительный GET-запрос для «прогрева» (если требуется)
        try:
            self.scraper.get("https://chat.deepseek.com", timeout=60)
        except Exception as e:
            print("Предварительный запрос для получения cookies не удался:", e)

    def _get_headers(self, pow_response: Optional[str] = None) -> Dict[str, str]:
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': f'Bearer {self.auth_token}',
            'content-type': 'application/json',
            'origin': 'https://chat.deepseek.com',
            'referer': 'https://chat.deepseek.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="120", "Google Chrome";v="120", "Not.A/Brand";v="8"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'x-app-version': '20241129.1',
            'x-client-locale': 'en_US',
            'x-client-platform': 'web',
            'x-client-version': '1.0.0-always',
        }
        if pow_response:
            headers['x-ds-pow-response'] = pow_response
        return headers

    def _make_request(self, method: str, endpoint: str, json_data: Dict[str, Any], pow_required: bool = False) -> Any:
        url = f"{self.BASE_URL}{endpoint}"

        try:
            headers = self._get_headers()
            if pow_required:
                challenge = self._get_pow_challenge()
                pow_response = self.pow_solver.solve_challenge(challenge)
                headers = self._get_headers(pow_response)

            response = self.scraper.request(
                method=method,
                url=url,
                headers=headers,
                json=json_data,
                timeout=None
            )

            if response.status_code == 401:
                raise AuthenticationError("Invalid or expired authentication token")
            elif response.status_code == 429:
                raise RateLimitError("API rate limit exceeded. Please wait before making more requests")
            elif response.status_code >= 500:
                raise APIError(f"Server error occurred: {response.text}", response.status_code)
            elif response.status_code != 200:
                raise APIError(f"API request failed: {response.text}", response.status_code)

            return response.json()

        except Exception as e:
            raise NetworkError(f"Network error occurred: {str(e)}")

    def _get_pow_challenge(self) -> Dict[str, Any]:
        try:
            response = self._make_request(
                'POST',
                '/chat/create_pow_challenge',
                {'target_path': '/api/v0/chat/completion'}
            )
            return response['data']['biz_data']['challenge']
        except KeyError:
            raise APIError("Invalid challenge response format from server")

    def create_chat_session(self) -> str:
        """Creates a new chat session and returns the session ID"""
        try:
            response = self._make_request(
                'POST',
                '/chat_session/create',
                {'character_id': None}
            )
            return response['data']['biz_data']['id']
        except KeyError:
            raise APIError("Invalid session creation response format from server")

    def chat_completion(self,
                        chat_session_id: str,
                        prompt: str,
                        parent_message_id: Optional[str] = None,
                        thinking_enabled: bool = True,
                        search_enabled: bool = False) -> Generator[Dict[str, Any], None, None]:
        """
        Send a message and get streaming response

        Args:
            chat_session_id (str): The ID of the chat session
            prompt (str): The message to send
            parent_message_id (Optional[str]): ID of the parent message for threading
            thinking_enabled (bool): Whether to show the thinking process
            search_enabled (bool): Whether to enable web search for up-to-date information

        Returns:
            Generator[Dict[str, Any], None, None]: Yields message chunks with content and type

        Raises:
            AuthenticationError: If the authentication token is invalid
            RateLimitError: If the API rate limit is exceeded
            NetworkError: If a network error occurs
            APIError: If any other API error occurs
        """
        if not prompt or not isinstance(prompt, str):
            raise ValueError("Prompt must be a non-empty string")
        if not chat_session_id or not isinstance(chat_session_id, str):
            raise ValueError("Chat session ID must be a non-empty string")

        json_data = {
            'chat_session_id': chat_session_id,
            'parent_message_id': parent_message_id,
            'prompt': prompt,
            'ref_file_ids': [],
            'thinking_enabled': thinking_enabled,
            'search_enabled': search_enabled,
        }

        try:
            # Решаем POW и получаем заголовки
            pow_challenge = self._get_pow_challenge()
            pow_response = self.pow_solver.solve_challenge(pow_challenge)
            headers = self._get_headers(pow_response=pow_response)

            response = self.scraper.post(
                f"{self.BASE_URL}/chat/completion",
                headers=headers,
                json=json_data,
                stream=True,
                timeout=None
            )

            if response.status_code != 200:
                error_text = next(response.iter_lines(), b'').decode('utf-8', 'ignore')
                if response.status_code == 401:
                    raise AuthenticationError("Invalid or expired authentication token")
                elif response.status_code == 429:
                    raise RateLimitError("API rate limit exceeded")
                else:
                    raise APIError(f"API request failed: {error_text}", response.status_code)

            for chunk in response.iter_lines():
                try:
                    parsed = self._parse_chunk(chunk)
                    if parsed:
                        yield parsed
                        if parsed.get('finish_reason') == 'stop':
                            break
                except Exception as e:
                    raise APIError(f"Error parsing response chunk: {str(e)}")

        except Exception as e:
            raise NetworkError(f"Network error occurred during streaming: {str(e)}")

    def _parse_chunk(self, chunk: bytes) -> Optional[Dict[str, Any]]:
        """Parse a SSE chunk from the API response"""
        if not chunk:
            return None

        try:
            if chunk.startswith(b'data: '):
                data = json.loads(chunk[6:])

                if 'choices' in data and data['choices']:
                    choice = data['choices'][0]
                    if 'delta' in choice:
                        delta = choice['delta']

                        return {
                            'content': delta.get('content', ''),
                            'type': delta.get('type', ''),
                            'finish_reason': choice.get('finish_reason')
                        }
        except json.JSONDecodeError:
            raise APIError("Invalid JSON in response chunk")
        except Exception as e:
            raise APIError(f"Error parsing chunk: {str(e)}")

        return None
