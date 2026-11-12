import json
def main():
    cfg = json.load(open('config/channel_config.json'))
    print("Would fetch videos from", cfg['reference_channel_url'])
if __name__ == '__main__':
    main()
