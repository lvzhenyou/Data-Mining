/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package classifier;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Yiting
 */
public class Classifier {

    private static String filePath;
    private static File originalFile;
    private static File trainFile;
    private static File testFile;
    private static PrintWriter predict;
    private static int totalTweets;
    private static Set<String> classNames;
    private static Map<String, Document> labelDoc;
    private static Map<String, Map<String, Double>> conditionalProbability;
    private static List<String> correctRes = new ArrayList<>();
    private static List<String> predictRes = new ArrayList<>();
    private static Map<String, Integer> tokenID = new HashMap<>();

    private static void split(InputStream input, OutputStream train, OutputStream test, double testRatio) throws IOException {
        while (true) {
            OutputStream output;
            if (Math.random() < testRatio) {
                output = test;
            } else {
                output = train;
            }
            int ch;
            do {
                ch = input.read();
                if (ch < 0) {
                    return;
                }
                output.write(ch);
            } while (ch != '\n');
        }
    }

    private static List sortByComparator(Map<Integer, Integer> unsortMap) {

        List<Map.Entry<Integer, Integer>> list = new ArrayList<>(unsortMap.entrySet());

        // sort list based on comparator
        Collections.sort(list, new Comparator<Map.Entry<Integer, Integer>>() {
            @Override
            public int compare(Map.Entry<Integer, Integer> o1, Map.Entry<Integer, Integer> o2) {
                return ((Integer) o1.getKey() - (Integer) o2.getKey());
            }
        });
        return list;
    }

    private static void createForSVM() {
        int ID = 1;
        for (Document trainDoc : labelDoc.values()) {
            for (Tweet tw : trainDoc.getTweets()) {
                for (String token : tw.getTokens()) {
                    if (!tokenID.containsKey(token)) {
                        tokenID.put(token, ID);
                        ID++;
                    }
                }
            }
        }
        for (Document trainDoc : labelDoc.values()) {
            int label = trainDoc.getLabelID();
            for (Tweet tw : trainDoc.getTweets()) {
                Map<Integer, Integer> tokenWithCount = new HashMap<>();
                for (String token : tw.getTokens()) {
                    if (trainDoc.getTokenCount(token) > 3) {
                        tokenWithCount.put(tokenID.get(token), trainDoc.getTokenCount(token));
                    }
                    //System.out.print(label + " " + tokenID.get(token) + ":" + trainDoc.getTokenCount(token) + " ");
                }
                List<Map.Entry<Integer, Integer>> list = sortByComparator(tokenWithCount);
                System.out.print(label + " ");
                for (int i = 0; i < list.size(); i++) {
                    System.out.print(list.get(i).getKey() + ":" + list.get(i).getValue() + " ");
                }
                System.out.println("");
            }
        }
    }

    public static Tweet getTweet(InputStream inputStream) throws IOException {
        Tweet tw = new Tweet();
        StringBuilder token = new StringBuilder();
        int ch = 0;
        while (true) {
            ch = inputStream.read();
            if (ch < 0) {
                return null;
            }
            if (ch >= 'a' && ch <= 'z') {
                token.append((char) ch);
            } else if (ch >= 'A' && ch <= 'Z') {
                token.append((char) (ch - 'A' + 'a'));
            } else if (token.length() > 1) {
                String tokenString = token.toString();
                token.delete(0, token.length());
                tw.addTokens(tokenString);
                //System.out.println(tokenString);
            }
            if (ch == '\n') {
                break;
            }
        }
        tw.setDocument(labelDoc.get(tw.removeLastToken()));
        return tw;
    }

    public static void constructSpecialTokens() {
        labelDoc.get("positive").setSpecialTokens("good");
        labelDoc.get("positive").setSpecialTokens("great");
        labelDoc.get("positive").setSpecialTokens("nice");
        labelDoc.get("negative").setSpecialTokens("sucks");
        labelDoc.get("negative").setSpecialTokens("awful");
        labelDoc.get("negative").setSpecialTokens("terrible");
    }

    public static void naive_bayesian_train(InputStream inputStream) throws IOException {
        int para = 1;
        totalTweets = 0;
        labelDoc = new HashMap<>();
        conditionalProbability = new HashMap<>();
        for (String labels : classNames) {
            labelDoc.put(labels, new Document(labels));
        }
        constructSpecialTokens();
        Tweet tw;
        while ((tw = getTweet(inputStream)) != null) {
            Document doc = tw.getDocument();
            if (doc != null) {
                doc.addOneTweet(tw);
                totalTweets++;
                for (String token : tw.getTokens()) {
                    //System.out.println(token);
                    if (!conditionalProbability.containsKey(token)) {
                        Map<String, Double> value = new HashMap<>();
                        conditionalProbability.put(token, value);
                    }
                }
            }
        }
        for (Document doc : labelDoc.values()) {
            doc.setPrior((double) doc.getTotalTokenCount() / totalTweets);
            for (Map.Entry<String, Map<String, Double>> entry : conditionalProbability.entrySet()) {
                String token = entry.getKey();
                double cond = (double) (doc.getTokenCount(token) + para) / (doc.getTotalTokenCount() + conditionalProbability.size());
                entry.getValue().put(doc.getName(), cond);
            }
        }
    }

    public static void naive_bayesian_test(InputStream inputStream, PrintWriter predict) throws IOException {
        Tweet tw;
        int correct = 0, incorrect = 0;
        while ((tw = getTweet(inputStream)) != null) {
            Document correctDoc = tw.getDocument();
            if (correctDoc != null) {
                Document predictDoc = null;
                double bestScore = -1;
                for (Document trainDoc : labelDoc.values()) {
                    double score = Math.log(trainDoc.getPrior());
                    for (String TokenInpredicTw : tw.getTokens()) {
                        //System.out.println(predicTw);
                        Map<String, Double> get = conditionalProbability.get(TokenInpredicTw);
                        if (get != null) {
                            score += Math.log(get.get(trainDoc.getName()));
                        }
                        if (trainDoc.containSpecialToken(TokenInpredicTw)) {
                            score += 10;
                        }
                    }
                    if (predictDoc == null || score > bestScore) {
                        predictDoc = trainDoc;
                        bestScore = score;
                    }
                    //System.out.println(bestScore);
                }
                predict.write(predictDoc.getName() + "\n");
                if (predictDoc == correctDoc) {
                    correct++;
                } else {
                    incorrect++;
                }
                correctRes.add(correctDoc.getName());
                predictRes.add(predictDoc.getName());
                //System.out.println(correctDoc.getName() + "\t" + predictDoc.getName());
            }
        }
        predict.close();
        double res = (double) correct / (incorrect + correct);
        System.out.println("Number of testing data: " + (correct + incorrect) + ", Correct=" + correct + ", Incorrect=" + incorrect + ", Accuracy=" + res);
        System.out.println("");
    }

    public static void analysis() {
        int res[][], preAll[], corAll[];
        double p[], r[], f[];
        res = new int[4][4];
        preAll = new int[4];
        corAll = new int[4];
        p = new double[4];
        r = new double[4];
        f = new double[4];
        for (int index = 0; index < correctRes.size(); index++) {
            String cT = predictRes.get(index);
            switch (correctRes.get(index)) {
                case "positive":
                    switch (cT) {
                        case "positive":
                            res[0][0]++;
                            preAll[0]++;
                            break;
                        case "negative":
                            res[0][1]++;
                            preAll[1]++;
                            break;
                        case "neutral":
                            res[0][2]++;
                            preAll[2]++;
                            break;
                        case "mixed":
                            res[0][3]++;
                            preAll[3]++;
                            break;
                    }
                    corAll[0]++;
                    break;
                case "negative":
                    switch (cT) {
                        case "positive":
                            res[1][0]++;
                            preAll[0]++;
                            break;
                        case "negative":
                            res[1][1]++;
                            preAll[1]++;
                            break;
                        case "neutral":
                            res[1][2]++;
                            preAll[2]++;
                            break;
                        case "mixed":
                            res[1][3]++;
                            preAll[3]++;
                            break;
                    }
                    corAll[1]++;
                    break;
                case "neutral":
                    switch (cT) {
                        case "positive":
                            res[2][0]++;
                            preAll[0]++;
                            break;
                        case "negative":
                            res[2][1]++;
                            preAll[1]++;
                            break;
                        case "neutral":
                            res[2][2]++;
                            preAll[2]++;
                            break;
                        case "mixed":
                            res[2][3]++;
                            preAll[3]++;
                            break;
                    }
                    corAll[2]++;
                    break;
                case "mixed":
                    switch (cT) {
                        case "positive":
                            res[3][0]++;
                            preAll[0]++;
                            break;
                        case "negative":
                            res[3][1]++;
                            preAll[1]++;
                            break;
                        case "neutral":
                            res[3][2]++;
                            preAll[2]++;
                            break;
                        case "mixed":
                            res[3][3]++;
                            preAll[3]++;
                            break;
                    }
                    corAll[3]++;
                    break;
            }
        }
        for (int[] label : res) {
            for (int value : label) {
                System.out.print(value + "\t");
            }
            System.out.println("");
        }
        System.out.println("");
        for (int i = 0; i < 4; i++) {
            p[i] = (double) res[i][i] / preAll[i];
            r[i] = (double) res[i][i] / corAll[i];
            f[i] = (2 * p[i] * r[i]) / (p[i] + r[i]);
            System.out.println("label " + (i + 1) + ": p=" + p[i] + ", r=" + r[i] + ", f=" + f[i] + "\t");
        }
    }

    public static void main(String[] args) throws IOException {
        int OP = 2;
        filePath = "/Users/Yiting/NetBeansProjects/Classifier/DATA/stock/";
        originalFile = new File(filePath, "training_oringal.txt");
        //trainFile = new File(filePath, "train.dat");
        //testFile = new File(filePath, "test.dat");
        trainFile = new File(filePath, "training_oringal.txt");
        testFile = new File(filePath, "Test_Stock.txt");
        predict = new PrintWriter(new BufferedWriter(new FileWriter("predict.dat", true)));
        classNames = new HashSet<>();
        classNames.add("positive");
        classNames.add("negative");
        classNames.add("neutral");
        classNames.add("mixed");
//        try {
//            FileInputStream input = new FileInputStream(originalFile);
//            FileOutputStream train = new FileOutputStream(trainFile);
//            FileOutputStream test = new FileOutputStream(testFile);
//            split(input, train, test, 0.1);
//        } catch (FileNotFoundException ex) {
//            Logger.getLogger(Classifier.class.getName()).log(Level.SEVERE, null, ex);
//        }
        try {
            if (OP == 1) {
                //FileInputStream trainInputStream = new FileInputStream(originalFile);
                FileInputStream trainInputStream = new FileInputStream(trainFile);
                FileInputStream testInputStream = new FileInputStream(testFile);
                naive_bayesian_train(trainInputStream);
                naive_bayesian_test(testInputStream, predict);
                analysis();
            } else if (OP == 2) {
                FileInputStream trainInputStream = new FileInputStream(trainFile);
                FileInputStream testInputStream = new FileInputStream(testFile);
                naive_bayesian_train(trainInputStream);
                createForSVM();
                System.out.println("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx");
                naive_bayesian_train(testInputStream);
                createForSVM();
            }

        } catch (FileNotFoundException ex) {
            Logger.getLogger(Classifier.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
}
