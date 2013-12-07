/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package classifier;

import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author Yiting
 */
public class Tweet {

    private Document document;
    private List<String> tokens = new ArrayList<>();

    public void setDocument(Document document) {
        this.document = document;
    }

    public Document getDocument() {
        return document;
    }

    public void addTokens(String token) {
        this.tokens.add(token);
    }

    public List<String> getTokens() {
        return this.tokens;
    }

    public String removeLastToken() {
        return this.tokens.remove(this.tokens.size() - 1);
    }
}
