using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Threading;
using UnityEngine;

public class TakeScreenShot : MonoBehaviour {
    string savePath = "Images/";
    Interprocess pyInterprocess = new Interprocess();
    string imageName = String.Empty;

    void Awake()
    {
        InvokeRepeating("TakeScreenshot", 1f, 5f);
    }

    private void TakeScreenshot()
    {
        //Call image processing
        pyInterprocess.getCoordinate(imageName);

        //time based name for a screenshot 
        imageName = DateTime.Now.ToString("MMddHHmmss") + ".png";

        // Take the screenshot
        ScreenCapture.CaptureScreenshot(savePath + imageName);
    }
}
