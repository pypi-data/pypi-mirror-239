import glob
feature_files = glob.glob('features/*.feature')

def line_exists(line, filename):
    with open(filename) as f:
        return line in f.read()

with open('fail_test') as qq_file, open(feature_files[0], 'r+') as data_file, open('features/flaky.feature', 'w+') as flaky:
    qq_lines = qq_file.readlines()
    data_lines = data_file.readlines()
    for line in qq_lines:
        line = line.strip()
        # 忽略空行
        if not line:
            continue
        for i in range(len(data_lines)):
            if line in data_lines[i]:
                # print(type(data_lines[i-1]))
                tmp = data_lines[i-1].split(" ")
                tmp.insert(-1, "@flaky")
                data_lines[i-1] = " ".join(tmp)
                print(data_lines[i-1])
    for i in data_lines:
        flaky.write(i)

print("處理完成。已在 data 檔案的對應 Scenario 上方加上 @flaky")
