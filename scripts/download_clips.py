import json
def main():
    cfg = json.load(open('config/channel_config.json'))
    print("Would download clips from", cfg['source_channels'])
if __name__ == '__main__':
    main()
