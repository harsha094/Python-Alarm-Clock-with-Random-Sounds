import time, random, pygame, os
from datetime import datetime

class AlarmClock:
    def __init__(self):
        pygame.mixer.init()
        sounds_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sounds')
        self.alarm_tones = {
            'beep': os.path.join(sounds_dir, 'beep.mp3'),
            'birds': os.path.join(sounds_dir, 'birds.mp3'),
            'TinSing': os.path.join(sounds_dir, 'TinSing.mp3')
        }
        self.alarms = []
        # Verify and print sound files status
        print("\nSound files status:")
        for tone, path in self.alarm_tones.items():
            print(f"{'✅' if os.path.exists(path) else '❌'} {tone}: {path}")

    def add_alarm(self, time_str, tone=None):
        try:
            alarm_time = datetime.strptime(time_str, "%H:%M").time()
            self.alarms.append({'time': alarm_time, 'tone': tone})
            print(f"Alarm set for {time_str}" + (f" with {tone} sound" if tone else " with random sound"))
        except ValueError:
            print("Invalid time format. Use HH:MM")

    def play_alarm(self, tone=None):
        try:
            sound_file = self.alarm_tones[tone] if tone in self.alarm_tones else random.choice(list(self.alarm_tones.values()))
            if os.path.exists(sound_file):
                print(f"🔔 ALARM! Playing: {sound_file}")
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play()
                time.sleep(30)  # Play for 30 seconds
                pygame.mixer.music.stop()
            else:
                print(f"⚠️ Sound file not found: {sound_file}\n\a")
        except Exception as e:
            print(f"Error playing sound: {e}\n\a")

    def check_alarms(self):
        current_time = datetime.now().time()
        for alarm in self.alarms[:]:
            if current_time.hour == alarm['time'].hour and current_time.minute == alarm['time'].minute:
                self.play_alarm(alarm['tone'])
                self.alarms.remove(alarm)

    def run(self):
        print("\nAlarm Clock Running... (Press Ctrl+C to exit)")
        print(f"Current alarms: " + ", ".join([f"{a['time'].strftime('%H:%M')} ({a['tone'] or 'random'})" for a in self.alarms]))
        try:
            while True:
                self.check_alarms()
                time.sleep(30)
        except KeyboardInterrupt:
            print("\nAlarm Clock stopped.")
            pygame.mixer.quit()

def main():
    clock = AlarmClock()
    # Set test alarm for 1 minute from now
    next_alarm = f"{datetime.now().hour:02d}:{(datetime.now().minute + 1) % 60:02d}"
    clock.add_alarm(next_alarm, "birds")
    clock.run()

if __name__ == "__main__":
    main()