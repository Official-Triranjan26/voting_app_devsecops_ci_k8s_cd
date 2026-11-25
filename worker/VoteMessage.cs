using Newtonsoft.Json;

namespace Worker
{
    public class VoteMessage
    {
        [JsonProperty("vote")]
        public string Vote { get; set; }

        [JsonProperty("voter_id")]
        public string VoterId { get; set; }

        public static VoteMessage Parse(string json)
        {
            return JsonConvert.DeserializeObject<VoteMessage>(json);
        }
    }
}
