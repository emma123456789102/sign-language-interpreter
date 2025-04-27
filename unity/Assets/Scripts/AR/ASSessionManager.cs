using UnityEngine;
using UnityEngine.XR.ARFoundation;

public class ARSessionManager : MonoBehaviour
{
    private ARSession arSession;

    void Start()
    {
        arSession = GetComponent<ARSession>();
        if (arSession == null)
        {
            Debug.LogError("ARSession component not found on this GameObject.");
            return;
        }

        // Start the AR session
        StartARSession();
    }

    public void StartARSession()
    {
        if (arSession != null && ARSession.state == ARSessionState.None)
        {
            arSession.Reset(); // Reset the session if needed
            arSession.enabled = true; // Enable the AR session
            Debug.Log("AR Session started.");
        }
    }

    public void StopARSession()
    {
        if (arSession != null && arSession.state != ARSessionState.None)
        {
            arSession.enabled = false; // Disable the AR session
            Debug.Log("AR Session stopped.");
        }
    }

    void OnEnable()
    {
        ARSession.stateChanged += OnARSessionStateChanged;
    }

    void OnDisable()
    {
        ARSession.stateChanged -= OnARSessionStateChanged;
    }

    private void OnARSessionStateChanged(ARSessionStateChangedEventArgs eventArgs)
    {
        switch (eventArgs.state)
        {
            case ARSessionState.SessionTracking:
                Debug.Log("AR Session is tracking.");
                // Handle session tracking state
                break;
            case ARSessionState.None:
                Debug.Log("AR Session is not running.");
                // Handle session not running state
                break;
            case ARSessionState.Ready:
                Debug.Log("AR Session is ready.");
                // Handle session ready state
                break;
            case ARSessionState.Failed:
                Debug.LogError("AR Session failed.");
                // Handle session failure
                break;
            // Add more cases as needed for other ARSessionStates
        }
    }
}
