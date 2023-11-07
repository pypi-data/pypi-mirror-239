"""Building the library"""
import setuptools

setuptools.setup(
    name="telegram_task",
    version="1.0.10",
    author="Arka Equities & Securities",
    author_email="info@arkaequities.com",
    description="A telegram bot task manager wrapper.",
    long_description="""
This project can be used as an interface for a simple task manager.
A telegram bot token and the ID of the manager account are the only \
essential input variables needed to enable this project as your \
personal assistant in running and handling jobs on a daily basis.
    """,
    packages=setuptools.find_packages(),
    install_requires=[
        "python-telegram-bot[socks,job-queue]==20.6",
        "python-dotenv==1.0.0",
        "pytz==2023.3.post1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
