using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class RasaConnector : MonoBehaviour
{
    private const string RasaEndpoint = "http://localhost:5005/webhooks/rest/webhook"; // Update with your Rasa server URL

    public void SendVisualDataToRasa(byte[] imageData)
    {
        StartCoroutine(SendDataCoroutine(imageData));
    }

    private IEnumerator SendDataCoroutine(byte[] imageData)
    {
        // this creates a form to send the image data
        WWWForm form = new WWWForm();
        form.AddBinaryData("image", imageData, "captured_image.png", "image/png");

        // and sending the POST request to the RASA server
        using (UnityWebRequest www = UnityWebRequest.Post(RasaEndpoint, form))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError($"Error sending data to Rasa: {www.error}");
            }
            else
            {
                Debug.Log("Visual data sent to Rasa successfully."); // handling the response from RASA if needed
                string response = www.downloadHandler.text;
                ProcessRasaResponse(response);
            }
        }
    }

    private void ProcessRasaResponse(string response)
    {
        // processes the response from RASA
        Debug.Log($"Rasa Response: {response}");
    }
}
