using UnityEngine;
using UnityEngine.XR.ARFoundation;
using UnityEngine.XR.ARSubsystems;

public class ARCameraFeed : MonoBehaviour
{
    private ARCameraManager cameraManager;
    private Texture2D cameraTexture;

    void Start()
    {
        cameraManager = GetComponent<ARCameraManager>();
        if (cameraManager == null)
        {
            Debug.LogError("ARCameraManager component not found on this GameObject.");
            return;
        }

        // subscribes to the frame received event
        cameraManager.frameReceived += OnCameraFrameReceived;
    }

    private void OnCameraFrameReceived(ARCameraFrameEventArgs eventArgs)
    {
        // this checks if the camera texture is available
        if (cameraManager.TryGetLatestImage(out XRCameraImage cameraImage))
        {
            // and this creates a Texture2D to hold the camera image
            if (cameraTexture == null || cameraTexture.width != cameraImage.width || cameraTexture.height != cameraImage.height)
            {
                cameraTexture = new Texture2D(cameraImage.width, cameraImage.height, TextureFormat.RGBA32, false);
            }

            // converting the camera image to a Texture2D
            cameraImage.Convert(cameraTexture.GetNativeTexturePtr(), cameraImage.format);
            cameraImage.Dispose();

            // processing the camera texture - like to send it to RASA
            ProcessCameraTexture(cameraTexture);
        }
    }

    private void ProcessCameraTexture(Texture2D texture)
    {
        // this will convert the texture to a byte array for sending to RASA
        byte[] imageData = texture.EncodeToPNG(); // or EncodeToJPG() for JPEG format

        Debug.Log("Captured camera frame and converted to byte array.");
    }

    void OnDestroy()
    {
        // Unsubscribe from the frame received event
        if (cameraManager != null)
        {
            cameraManager.frameReceived -= OnCameraFrameReceived;
        }
    }
}
