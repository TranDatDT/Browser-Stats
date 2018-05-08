from operator import itemgetter
from ua_parser import user_agent_parser


def seg_access_log(line):
    delimiters = {'[': ']', '"': '"'}
    idx, start, count, delimiter, results = 0, 0, len(line), ' ', []

    while True:
        idx = line.find(delimiter, start)
        delimiter = ' '  # reset
        if idx < 0:
            break

        if start < idx:
            results.append(line[start:idx])
        start = idx + 1
        # if idx != count - 1 and line[idx + 1] in delimiters:
        if line[idx + 1] in delimiters:
            delimiter = delimiters[line[idx + 1]]
            start += 1

    if start < count:
        results.append(line[start:].rstrip())

    return results


def solve():
    browsers = {}

    with open("data/data-01.txt") as f:
        for line in f.readlines():
            ua_string = seg_access_log(line)[-4]
            parsed_string = user_agent_parser.ParseUserAgent(ua_string)
            browser = parsed_string["family"]
            if browser == "Facebook":
                print(browser)
            if browser not in browsers:
                browsers[browser] = 1
            else:
                browsers[browser] += 1

    total_browsers = sum(browser for browser in browsers.values())

    for browser in browsers:
        browsers[browser] = "{0:.2f}%".format(100 * browsers[browser] / total_browsers)

    del total_browsers

    return browsers


def main():
    data = solve()
    browsers = sorted(data.items(), key=itemgetter(1), reverse=True)
    for browser, ratio in browsers:
        print(ratio, browser)


if __name__ == '__main__':
    main()
