package JavaExtractor.FeaturesEntities;

import java.util.ArrayList;
import java.util.stream.Collectors;

import com.fasterxml.jackson.annotation.JsonIgnore;

public class ProgramFeatures {
    private String name;
    private boolean isPositive;
    private boolean isDefault;

    private ArrayList<ProgramRelation> features = new ArrayList<>();

    //isPositive : whether it is a positive sample (true) or negative (false)
    public ProgramFeatures(String name, boolean isPositive) {
        this.name = name;
        this.isPositive = isPositive;
        isDefault = false;
    }

    public ProgramFeatures(String name) {
        this.name = name;
        isDefault = true;
    }

    @SuppressWarnings("StringBufferReplaceableByString")
    @Override
    public String toString() {
        StringBuilder stringBuilder = new StringBuilder();
        // Tushar: We dont need name as the target embedding because we are transforming it to the classification job
        //stringBuilder.append(name).append(" ");
        if (isDefault)
            stringBuilder.append(name).append(" ");
        else
            stringBuilder.append(isPositive).append(" ");
        //----
        stringBuilder.append(features.stream().map(ProgramRelation::toString).collect(Collectors.joining(" ")));

        return stringBuilder.toString();
    }

    public void addFeature(Property source, String path, Property target) {
        ProgramRelation newRelation = new ProgramRelation(source, target, path);
        features.add(newRelation);
    }

    @JsonIgnore
    public boolean isEmpty() {
        return features.isEmpty();
    }

    public void deleteAllPaths() {
        features.clear();
    }

    public String getName() {
        return name;
    }

    public ArrayList<ProgramRelation> getFeatures() {
        return features;
    }

}
