## Dataset
This is the dataset for our paper *Choice-75: A Dataset on Decision Branching in Script Learning*.

### Overall Structure
- `dataset_key.json`: stores the mapping from `goal` to `split` (e.g. `train`, `dev`, `test`); the `goal` is the goal from `proScript` (Note that `test` data annotation is not provided in the current version)
- `index_key.json`: stores the mapping from `goal` to index, which is used to name `.json` files (e.g. script #1 => `1.json`).
- `user_profile`, `verb_phrase_manual`, `verb_phrase_machine`: folders for the data, organized by split

### Data Fields
- `goal`: text from `proScript` (str)
- `steps`: list of steps (list[str])
- `original_index`: original index in the `proScript` dataset
- `index`: index in our file system (i.e. the following example would be `5.json`)
- `branching_info`: branching-related daata fields
	- `branching_step`: the step that has branches  
	- `branching_idx`: index of `branching_step` in the original `steps` list
	- `option 1`, `option 2`: two options for the `branching_step` 
	- `dataset`: dataset split
	- `freeform_ra`: scenarios, each scenario data point consists of [scenario, ground truth option, level of difficulties].

**Note:** you can safely disregard any field that is not noted above, they are not related to the current phase of this project.

```
{
    "goal": "work at a ramen shop",
    "steps": [
        "decided to work at a ramen shop",
        "write a resume",
        "write a cover letter",
        "submit resume and cover letter to the ramen shop",
        "wait for the ramen shop to get in touch",
        "go in for an interview",
        "accept a job offer"
    ],
    "original_index": 552,
    "curr_index": 6157,
    "index": 5,
    "branching_info": {
        "branching_idx": 3,
        "branching_step": "submit resume and cover letter to the ramen shop",
        "option 1": "print out everything and submit them to the ramen shop in person",
        "option 2": "submit the resume and cover letter online",
        "type": "golden",
        "dataset": "dev",
        "freeform_ra": [
            [
                "have additional questions about the position",
                1,
                "medium"
            ],
            [
                "have no printer",
                2,
                "easy"
            ],
            [
                "live far away from the ramen shop",
                2,
                "easy"
            ],
            [
                "want to make a good impression",
                1,
                "medium"
            ],
            [
                "is a fan of japanese culture",
                0,
                "na"
            ]
        ]
    }
}
```


### References
- Keisuke Sakaguchi, Chandra Bhagavatula, Ronan Le Bras, Niket Tandon, Peter Clark, and Yejin Choi. 2021. [*proScript: Partially Ordered Scripts Generation*](https://aclanthology.org/2021.findings-emnlp.184). In Findings of the Association for Computational Linguistics: EMNLP 2021, pages 2138–2149, Punta Cana, Dominican Republic. Association for Computational Linguistics.
