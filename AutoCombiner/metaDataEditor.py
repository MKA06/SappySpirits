import json

ipfsCID = "ipfs://QmSz2Ke4ZuGZnPpz8GtgBH8fweoVxk8XCpGh65ynZwmCJw"
img_num = 444

for i in range(img_num):
    with open(f"./jsonfiles/{i+1}.json", "r+") as f:
        data = json.load(f)
        data["image"] = f"{ipfsCID}/SappySpirit-{i+1}.png"
        f.seek(0)
        json.dump(data, f, indent=1)
        f.truncate()


