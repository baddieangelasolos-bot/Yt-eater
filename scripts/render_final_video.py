import json
def main():
    cfg = json.load(open('config/channel_config.json'))
    print("Would render video with resolution", cfg['output_resolution'])
if __name__ == '__main__':
    main()
