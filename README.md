# gallery-dl Multi-Instance Downloader
 
 ‍


Description:

Allows you to run multiple instances of gallery-dl to allow for multi-threaded downloading, increasing download speeds drastically

For example 64 instances can download up to 64 times faster and will all download one URL each from a provided CSV file that contains folder name and url.

It will also create a error log csv file to store all the ones that it failed to download. It is recommended to check these for domains that are valid but gallery-dl couldn't download and do these manually, excluding dead domains.

You can estimate to download around 40k images in 1~2 hours with 64 instances at ~15 MB/s, although you will need a decent CPU to keep up with the load (this is only an assumption and not based off real measurements).

No support for operating systems other than Windows.
 
 ‍


Prep:

An example use case for this is that you would scrape multiple forum threads for all the image and video URLs and save them to a CSV file with the column names of 'title' and 'url'. You will provide the thread title and a file URL in a pair which will be used to store the files in a folder under that title.

If you are inexperienced in scraping or aren't good at programming then I recommend you to use a program named [Octoparse](https://www.octoparse.com). Learn how to scrape data and provide an xpath for the URL contents you want to capture in the HTML. You may need their professional premium trial which does provide you with 20 Cloud PC instances to scrape on to gather data fast, and also allows you to export a high amount of lines/data. This is what I use.
 
 ‍


Usage:

1. When you run the python file you will be asked to provide the main folder where all your files will be grouped into folders.

2. You will provide your CSV file with the columns "title" and "url" which provide the containing folder's name your files will be placed in.

3. You will then provide a location to where your error log CSV file will go, this will contain the 'error', 'title', and 'url' columns.

4. You will provide the number of instances you want to run of the program, the more you run the heavier it will be on your CPU but the more files it will download in parallel and faster they will all download (personally I use '96' on a Ryzen 9 5950X)

5. When it is all complete you will see "Done. Press Enter to finish...", keep it running until then, that means it finished downloading everything.

Note: Once it starts running the instances you should avoid stopping it but if you must close the command line window to stop it running more commands.
