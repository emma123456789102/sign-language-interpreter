using UnityEngine;

public class UIManager : MonoBehaviour
{
    [SerializeField]
    private GameObject mainMenuPanel; // Reference to the main menu panel
    [SerializeField]
    private GameObject arSessionPanel; // Reference to the AR session panel
    [SerializeField]
    private GameObject loadingPanel; // Reference to the loading panel
    [SerializeField]
    private GameObject errorPanel; // Reference to the error panel

    private void Start()
    {
        ShowMainMenu(); // Show the main menu at the start
    }

    public void ShowMainMenu()
    {
        SetActivePanel(mainMenuPanel);
    }

    public void StartARSession()
    {
        SetActivePanel(arSessionPanel);
        // Optionally, start the AR session here
    }

    public void ShowLoadingScreen()
    {
        SetActivePanel(loadingPanel);
    }

    public void ShowErrorScreen(string errorMessage)
    {
        SetActivePanel(errorPanel);
        // Update the error message in the error panel if needed
        // For example, you can have a Text component in the error panel to display the message
        // errorPanel.GetComponentInChildren<Text>().text = errorMessage;
    }

    private void SetActivePanel(GameObject panelToActivate)
    {
        // Deactivate all panels
        mainMenuPanel.SetActive(false);
        arSessionPanel.SetActive(false);
        loadingPanel.SetActive(false);
        errorPanel.SetActive(false);

        // Activate the selected panel
        if (panelToActivate != null)
        {
            panelToActivate.SetActive(true);
        }
    }
}
