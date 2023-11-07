
import email


e = email.message_from_file(open('test/fixtures/headered.file'))
for l in dir(e):
    print(l)

print("BODY")

for part in e.walk():
    print(part)
