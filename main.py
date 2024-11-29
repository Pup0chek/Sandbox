import base64

from core.VirusTotalAPI import Upload_file, Get_File_Info





def main():
        id = Upload_file("test.txt").get("id")
        decoded = base64.b64decode(id).decode('utf-8')
        splited = decoded.split(":")
        print(Get_File_Info(splited[0]))


if __name__ == "__main__":
    main()