#!/usr/bin/env python
import os
import sys




print('''
a mantra for the software to say before it does anything, and also anyone who works on the system
server mantra: 'we are weaving golden webs'
server name: dreamweaver
'''
)

print("the build cries out, please, don't break me!")

print("what if we made the code self-writing, by making the system facilitate the writing of tests and stuff")

print("what if you can't really run the local devserver at all?")
print("what if this codebase guides you into running the tests frequently")


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
