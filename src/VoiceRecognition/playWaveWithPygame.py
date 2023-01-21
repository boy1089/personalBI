import pygame
import librosa, librosa.display 
 

    


# 스크린 전체 크기 지정

SCREEN_WIDTH = 400
SCREEN_HEIGHT  = 500

 

pygame.init()




# 스크린 객체 저장
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("pygame sount test")

 

clock = pygame.time.Clock()

path = r"D:\python\7. logger2\logger\data\voice\형_01031373281_20220219115430.wav"

# sig, sr = librosa.load(path, sr=22050, duration = 60)
# n_fft = 2048
# hop_length = 1024
# spec_mag = abs(librosa.stft(sig, n_fft=n_fft, hop_length=hop_length))



img = pygame.image.load(r"D:\python\7. logger2\logger\data\image\images_2022-03-07\20220307_153910.jpg")
SCREEN.blit(img, (0, 0))

pygame.mixer.music.load(path)

sound_thunder = pygame.mixer.Sound(path)

pygame.mixer.music.play(-1)

 

# playing = True
# while playing:
#     for event in pygame.event.get():

#         if event.type == pygame.QUIT:
#             playing = False
#             pygame.quit()


#         if event.type == pygame.KEYDOWN:

#             if event.key == pygame.K_UP:
#                 v = pygame.mixer.music.get_volume()
#                 pygame.mixer.music.set_volume(v + 0.1)
#                 print("volume up")

#             if event.key == pygame.K_DOWN:
#                 v = pygame.mixer.music.get_volume()
#                 pygame.mixer.music.set_volume(v - 0.1)
#                 print("volume down")

#             if event.key == pygame.K_LEFT:
#                 pygame.mixer.music.pause()
#                 print("일시 멈춤")

 

#             if event.key == pygame.K_RIGHT:
#                 pygame.mixer.music.unpause()
#                 print("다시 재생")
                
#             if event.key == pygame.K_a:
#                 sound_thunder.play()
#                 print("천둥소리")


#     # 1초에 60번의 빈도로 순환하기
#     clock.tick(60)