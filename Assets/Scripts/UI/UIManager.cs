using UnityEngine;

public class UIManager : MonoBehaviour
{
    [SerializeField]
    private GameObject mainMenuPanel; // this references to the main menu panel
    [SerializeField]
    private GameObject arSessionPanel; // referencing the AR session panel
    [SerializeField]
    private GameObject loadingPanel; // referencing the loading panel
    [SerializeField]
    private GameObject errorPanel; // referencing the error panel

    private void Start()
    {
        ShowMainMenu(); // this shows the main menu at the start
    }

    public void ShowMainMenu()
    {
        SetActivePanel(mainMenuPanel);
    }

    public void StartARSession()
    {
        SetActivePanel(arSessionPanel);
    }

    public void ShowLoadingScreen()
    {
        SetActivePanel(loadingPanel);
    }

    private void SetActivePanel(GameObject panelToActivate)
    {
        // this deactivates all panels
        mainMenuPanel.SetActive(false);
        arSessionPanel.SetActive(false);
        loadingPanel.SetActive(false);
        errorPanel.SetActive(false);

        // and this activates the selected panel
        if (panelToActivate != null)
        {
            panelToActivate.SetActive(true);
        }
    }
}
