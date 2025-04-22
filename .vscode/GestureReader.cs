using UnityEngine;
using UnityEngine.Networking;
using System.Collections;

public class GestureReader : MonoBehaviour
{
    string url = "http://127.0.0.1:5000/gesture";
    if (www.result != UnityWebRequest.Result.Success)
{
    Debug.LogError("Error: " + www.error);
}
    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(GetGesture());
    }
    // Update is called once per frame

    IEnumerator Start()
    {
        while (true)
        {
            UnityWebRequest www = UnityWebRequest.Get(url);
            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.Success)
            {
                string json = www.downloadHandler.text;
                Debug.Log("Gesture: " + json);
                // You can parse it with JsonUtility if needed
            }
            yield return new WaitForSeconds(0.2f); // Adjust frequency
        }
    }
}
