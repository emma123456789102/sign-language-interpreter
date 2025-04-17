using UnityEngine;
using UnityEngine.Networking;
using System.Collections;

public class GestureFetcher : MonoBehaviour
{
    void Start()
    {
        StartCoroutine(GetGesture());
    }

    IEnumerator GetGesture()
    {
        while (true)
        {
            UnityWebRequest www = UnityWebRequest.Get("http://localhost:5000/gesture");
            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.Success)
            {
                string json = www.downloadHandler.text;
                GestureData gesture = JsonUtility.FromJson<GestureData>(json);
                Debug.Log("Current Gesture: " + gesture.gesture);
                // TODO: Display or use gesture data in your Unity HUD
            }
            else
            {
                Debug.LogError("Error: " + www.error);
            }

            yield return new WaitForSeconds(0.5f); // poll every 0.5s
        }
    }
}

[System.Serializable]
public class GestureData
{
    public string gesture;
}
