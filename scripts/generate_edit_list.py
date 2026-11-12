import json
def main():
    cfg = json.load(open('config/channel_config.json'))
    print("Would generate edit list using", cfg['clip_duration'], "seconds per clip")
if __name__ == '__main__':
    main()
