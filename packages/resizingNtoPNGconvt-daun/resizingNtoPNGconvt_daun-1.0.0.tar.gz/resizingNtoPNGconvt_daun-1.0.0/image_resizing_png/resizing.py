from PIL import Image
import os

print('원본이미지 파일이 있는 폴더명을 입력하세요.')
path = input()
print(path,'저장할 폴더명을 입력하세요.')
path2 = input()

raw_path = path         # 원본 이미지 폴더 경로
save_path = path2       # 저장할 이미지 경로

# 저장폴더가 없을 경우 생성
if not os.path.exists(save_path):
    os.mkdir(save_path)

for file in os.listdir(raw_path):
    im = Image.open(raw_path+file)  # 이미지 파일 열기

    newWidth = 1000
    newHeight = 500

    # 1MB 초과 이미지 리사이즈
    if((os.path.getsize(raw_path+file)/(1024.0 * 1024.0)) > 1):
        print('file 사이즈 : ' , "%2.f MB" % (os.path.getsize(raw_path+file)/(1024.0 * 1024.0)))

        # 사이즈별 가로/세로 재설정
        if im.width > im.height :       # 원본이미지 : 가로 > 세로 일때
            if im.width > newWidth :     # 원본 가로가 1000 이상일 때
                newHeight = (im.height * newWidth) / im.width

        if im.height > im.width :       # 원본이미지 : 세로 > 가로 일때
            if im.height > newHeight :  # 원본 세로가 500 이상일 때
                newWidth = (im.width * newHeight) / im.height
        
        # 리사이즈
        im = im.resize((int(newWidth), int(newHeight)))

    # 이미지 PNG로 저장
    im = im.convert('RGB')
    filename, file_extension = os.path.splitext(file)
    im.save(save_path + filename+ ".png")

print('이미지 convert 완료!')