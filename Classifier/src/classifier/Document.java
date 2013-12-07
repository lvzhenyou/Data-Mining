/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package classifier;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 *
 * @author Yiting
 */
public class Document {

    private String label;
    private int labelID;
    private int totalTokenCount = 0;
    private double prior;
    private List<Tweet> tweets = new ArrayList<>();
    private Map<String, Integer> tokenCounter = new HashMap<>();
    private Set<String> specialTokens = new HashSet<>();

    public Document(String name) {
        this.label = name;
        if ("positive".equals(name)) {
            labelID = 1;
        }
        if ("negative".equals(name)) {
            labelID = 2;
        }
        if ("neutral".equals(name)) {
            labelID = 3;
        }
        if ("mixed".equals(name)) {
            labelID = 4;
        }
    }

    public String getName() {
        return label;
    }

    public int getLabelID(){
        return this.labelID;
    }
    public int getTotalTokenCount() {
        return totalTokenCount;
    }

    public int getTweetsCount() {
        return tweets.size();
    }

    public int getTokenCount(String token) {
        Integer count = tokenCounter.get(token);
        if (count == null) {
            return 0;
        }
        return count;
    }

    public void addOneTweet(Tweet tw) {
        tweets.add(tw);
        List<String> tokens = tw.getTokens();
        totalTokenCount += tokens.size();
        for (String token : tokens) {
            Integer count = tokenCounter.get(token);
            if (count == null) {
                count = 1;
            } else {
                count++;
            }
            tokenCounter.put(token, count);
        }
    }

    public List<Tweet> getTweets() {
        return this.tweets;
    }

    public void setPrior(double prior) {
        this.prior = prior;
    }

    public double getPrior() {
        return prior;
    }

    public void setSpecialTokens(String token) {
        this.specialTokens.add(token);
    }

    boolean containSpecialToken(String token) {
        return this.specialTokens.contains(token);
    }
}
