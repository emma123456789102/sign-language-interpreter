using UnityEngine;

[System.Serializable]
public class SignLanguageDataModel
{
    public string user_id; // this is where the ID of the user sending the sign language data goes (at the time of writing this I did not know the syntax to put down)
    public string sign; // the sign being performed - like the specific gesture

    // this acts as the constructor for easy initialisation
    public SignLanguageDataModel(string userId, string sign, string context, float timestamp)
    {
        this.user_id = userId;
        this.sign = sign;
        this.context = context;
        this.timestamp = timestamp;
    }
}
