from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import cv2
import pygame
import keyboard
import threading
import pkg_resources


def play_video():
    def block_keyboard():
        for i in range(150):
            keyboard.block_key(i)

    def unblock_keyboard():
        for i in range(150):
            keyboard.unblock_key(i)

    def play_audio():
        audio='assets/audio.mp3'
        try:
            audio_path = pkg_resources.resource_filename('thugshaker', audio)
        except FileNotFoundError and ModuleNotFoundError:
            audio_path = audio
            
        try:
            pygame.init()
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except pygame.error as e:
            print(f"An error occurred: {e}")
        finally:
            pygame.quit()

    def play_video():
        video = "assets/video.mp4"
        try:
            video_path = pkg_resources.resource_filename('thugshaker', video)
        except FileNotFoundError and ModuleNotFoundError:
            video_path = video
            
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print("Error: Could not open video.")
            return

        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

        cv2.namedWindow("thugshaker", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("thugshaker", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        frame_rate = 30
        frame_delay = int(1000 / frame_rate)

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            cv2.imshow("thugshaker", frame)
            if cv2.waitKey(frame_delay) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    audio_thread = threading.Thread(target=play_audio)
    video_thread = threading.Thread(target=play_video)

    block_keyboard()

    audio_thread.start()
    video_thread.start()

    audio_thread.join()
    video_thread.join()

    unblock_keyboard()
    
def main():
    play_video()
        
if __name__ == "__main__":
    main()