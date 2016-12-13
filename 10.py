import re

goes_regex = re.compile("value (\d+) goes to bot (\d+)")
gives_regex = re.compile("bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)")


class Bot(object):
    def __init__(self, name):
        self.name = name
        self.chips = []
        self.higher = None
        self.lower = None

    def give(self, bots, outputs):
        a = self.chips.pop()
        b = self.chips.pop()

        high = max(a, b)
        if self.higher[0] == 'bot':
            bots[self.higher[1]].receive(high)
        else:
            outputs[self.higher[1]] = high

        low = min(a, b)
        if self.lower[0] == 'bot':
            bots[self.lower[1]].receive(low)
        else:
            outputs[self.lower[1]] = low

    def receive(self, chip):
        self.chips.append(chip)
        if 61 in self.chips and 17 in self.chips:
            print self.name


bots = [
    Bot('bot %d' % i)
    for i in xrange(1000)
]
outputs = [
    None
    for i in xrange(100)
]

# Load settings
with open('10.txt') as f:
    for line in f:
        if goes_regex.match(line):
            value, bot = goes_regex.match(line).groups()
            bots[int(bot)].receive(int(value))
        elif gives_regex.match(line):
            giving_num, low_type, low_num, high_type, high_num = gives_regex.match(line).groups()
            giving_bot = bots[int(giving_num)]
            giving_bot.higher = (high_type, int(high_num))
            giving_bot.lower = (low_type, int(low_num))
        else:
            print "Parse failed: %s" % line

# Iterate
while True:
    idle = True
    for bot in bots:
        if len(bot.chips) == 2:
            bot.give(bots, outputs)
            idle = False
            break
    if idle:
        break

print "Outputs: %s" % outputs
