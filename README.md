# Dataset

Statsbomb free data was used, dropping events outside the 1st half.

# Methodology

The idea was to train based on the sequence of Statsbomb events, each of which has their own ID, subevents and fields. This is explained in their data specification.
For each match, event dictionaries are flattened into standarized fields built from the dataset vocabulary. A match dict has various categorical fields
and a single numerical field, which contains a 2D array where the outermost dimension is the number of events T and the innermost dimension is variable.
Each categorical field contains a vector (sequence) of length T (number of events) where the values are event IDs.

The reason for having a separate categorical fields and a single numerical one for each event is that each categorical field needs its own embedding layer to correctly
express the semantics of the category ID they hold, while numerical values don't need such transformation and can be simply projected.

## Model
When all categorical input fields for an event T have been embedded, they are concatenated to a fixed-size projection of the numerical input field.
At this point, the match is basically a matrix of shape (events, embedding length). This is passed to a Self-Attention layer. The ouput is flattened
and classified by dense layers into Home win, Away win or Draw using Softmax, with Sparse Categorical Crossentropy as the loss function

# Results analysis
I segmented test samples into two experiments: One where the halftime result holds at fulltime and other where the fulltime result is different from
the one at halftime. Sadly, the contrast shows that the model learns to assume that whatever was the result at halftime will be the one at fulltime,
being it clear that it randomly guesses in the test matches where HT result != FT result. This could indicate either a failure in the data preparation or
the model architecture, or more simply just illustrate how football results are greatly caused by randomness and can't be reliably parameterized.

## WHEN RESULT HOLDS
              precision    recall  f1-score   support

        HOME       0.88      0.82      0.85        95
        AWAY       0.83      0.87      0.85        98
        DRAW       0.70      0.72      0.71        95

    accuracy                           0.80       288
   macro avg       0.80      0.80      0.80       288
weighted avg       0.80      0.80      0.80       288

## WHEN RESULT DOESN'T HOLD
              precision    recall  f1-score   support

        HOME       0.34      0.22      0.27        64
        AWAY       0.33      0.30      0.31        61
        DRAW       0.18      0.27      0.22        64

    accuracy                           0.26       189
   macro avg       0.29      0.26      0.26       189
weighted avg       0.28      0.26      0.26       189
