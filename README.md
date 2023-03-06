<h1>Backups</h1>

<p>This is an automated full and incremental backups program written in Python. It allows the user to input a source directory and destination directory and it performs a full, if it's the first time performing the backup or an incremental backup in case a backup already exists. The program stores a log called backup.pkl inside the folder generate for the backup.</p>

<h2>Installation</h2>

<p>To use this program, you need to have Python 3 installed on your system. You can download Python from the official website: <a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a></p>

<p>You also need to import the os, shutil, hashlib, pickle, datetime and pretty table modules. </p>


<h2>Usage</h2>

<p>To use the program, simply run the backup.py file in your terminal:</p>

<pre><code>python backup.py</code></pre>

<p>You will be prompted to enter a URL, and the program will generate a shortened URL for you. The program will also open the shortened URL in your default web browser.</p>

<h2>Contributing</h2>

<p>If you find any bugs or issues with the program, feel free to open an issue on the GitHub repository.</p>
