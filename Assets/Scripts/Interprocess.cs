using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;
using System.IO;

public class Interprocess : MonoBehaviour {

    public string coordinates = string.Empty;

    // full path of python interpreter 
    //¡¡Important!! your need configure this PATH
    string python = @"C:\Program Files (x86)\Python35-32\python.exe";

    // python app to call 
    string pythonScript = @"F:\Desarrollo\PythonUnity\Assets\Scripts\imageProcessing.py";

    public string getCoordinate(string fileName)
    {

        // Create new process start info 
        ProcessStartInfo myProcessStartInfo = new ProcessStartInfo(python);

        // make sure we can read the output from stdout 
        myProcessStartInfo.UseShellExecute = false;
        myProcessStartInfo.RedirectStandardOutput = true;
        myProcessStartInfo.CreateNoWindow = true;

        // start python app with 3 arguments  
        // 1st arguments is pointer to itself,  
        // 2nd is a actual argument we want to send 
        myProcessStartInfo.Arguments = pythonScript + " " + fileName.ToString() ;

        Process pyProcess = new Process();
        // assign start information to the process 
        pyProcess.StartInfo = myProcessStartInfo;

        UnityEngine.Debug.Log("Calling Python script with arguments {0} "+fileName);

        // start the process 
        pyProcess.Start();

        // Read the standard output of the app we called.  
        // in order to avoid deadlock we will read output first 
        // and then wait for process terminate: 
        StreamReader myStreamReader = pyProcess.StandardOutput;
        string coordinates = myStreamReader.ReadLine();

        /*if you need to read multiple lines, you might use: 
            string coordinates = myStreamReader.ReadToEnd() */

        // wait exit signal from the app we called and then close it. 
        pyProcess.WaitForExit();
        pyProcess.Close();

        // write the output we got from python app 
        UnityEngine.Debug.Log(coordinates);
        return coordinates;
    }
}
