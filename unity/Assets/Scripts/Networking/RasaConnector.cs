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
        // Create a form to send the image data
        WWWForm form = new WWWForm();
        form.AddBinaryData("image", imageData, "captured_image.png", "image/png");

        // Send the POST request to the Rasa server
        using (UnityWebRequest www = UnityWebRequest.Post(RasaEndpoint, form))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError($"Error sending data to Rasa: {www.error}");
            }
            else
            {
                Debug.Log("Visual data sent to Rasa successfully.");
                // Handle the response from Rasa if needed
                string response = www.downloadHandler.text;
                ProcessRasaResponse(response);
            }
        }
    }

    private void ProcessRasaResponse(string response)
    {
        // Process the response from Rasa
        Debug.Log($"Rasa Response: {response}");
        // You can parse the response and update your UI or game state accordingly
    }
}
