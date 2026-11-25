using System;
using Worker;
using Xunit;

namespace Worker.UnitTests
{
    public class VoteMessageTests
    {
        [Fact]
        public void ParseReadsVoteAndVoterIdFromRedisMessage()
        {
            var message = VoteMessage.Parse("{\"vote\":\"a\",\"voter_id\":\"voter-123\"}");

            Assert.Equal("a", message.Vote);
            Assert.Equal("voter-123", message.VoterId);
        }

        [Fact]
        public void ParseRejectsMalformedJson()
        {
            Assert.Throws<Newtonsoft.Json.JsonReaderException>(() => VoteMessage.Parse("not-json"));
        }
    }
}
