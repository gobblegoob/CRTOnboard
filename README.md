<h1># CRTOnboard V2.0</h1>
<h2>Bulk import and organize Secure CRT Sessions from a CSV</h2>

Support has been added for arguments as well as creating a Class for a CRT object.  
The script can now be more easily executed as well as referenced from other programs such as a future simple GUI.

CRTOnboard takes a source csv file and creates a directory of of SecureCRT sessions.

This allows you to bulk create many sessions in an organized and consistant way.  You can also use exports from NAC, Solarwinds, Cisco Prime, or other software to build your import lists.  

To create a new source csv file, use the following headers in your CSV or the included template: 
HOSTNAME,HOST_IP,USERNAME,BUILDING,IDF

<b>Optional arguments:</b>
<ul style="list-style-type:none;">
  <li>-h, --help            show this help message and exit</li>
  <li>-c CLIENT, --client CLIENT
                        Name of the client</li>
  <li>-f FILE, --file FILE  Enter file name for source CSV</li>
  <li>-p PATH, --path PATH  Optional enter destination path for session folder</li>
</ul>
<b>How do I use it?</b>
<ul style="list-style-type:none;">
 <li> Execute script providing arguments.  Be advised, your directory slashes may need to be escaped.</li>
 <li> Edit CRTOnboard.py path variables for your respective SecureCRT Session library. The path variable is:
    - root_path</li>
 <li> Add your network devices to the the crtsource.csv file as completely as possible.</li>
 <li> Execute crtonboard.py and follow on screen prompts.</li>
 <li> You may need to close and relaunch SecureCRT to populate the list</li>
 <li> Log files are stored in each created directory so they can be easily located.</li>
</ul>
