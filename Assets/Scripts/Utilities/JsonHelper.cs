using System.Collections.Generic;
using UnityEngine;

public static class JsonHelper
{
    // serialises an object to a JSON string
    public static string ToJson<T>(T obj)
    {
        return JsonUtility.ToJson(obj);
    }

    // deserialises a JSON string to an object
    public static T FromJson<T>(string json)
    {
        return JsonUtility.FromJson<T>(json);
    }

    // deserialising a JSON string to a list of objects
    public static List<T> FromJsonList<T>(string json)
    {
        // this creates a wrapper class to hold in the list
        Wrapper<T> wrapper = JsonUtility.FromJson<Wrapper<T>>(json);
        return wrapper.Items;
    }

    // the wrapper class for deserialising this lists
    [System.Serializable]
    private class Wrapper<T>
    {
        public List<T> Items;
    }
}
