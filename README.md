# A Dataset for The Global Artificial Intelligence Championship
![odyssey](./docs/odyssey.webp)

GAIC Math 2024 presents a collection of 387 meticulously crafted math problems, meticulously curated by professional math problem writers from both universities and high schools. The compilation includes high school competition questions with 148 problems, followed by a series of 138 high school mathematics questions, and concluding with 101 university-level mathematics questions. 

The GAIC Math 2024 problem setter committee is composed of mathematics professors hailing from esteemed institutions such as Arizona State University, Johns Hopkins University, Drexel University, National University of Singapore, Tsinghua University, and Central China Normal University. These professors were formally invited by AGI Odyssey to contribute their expertise to the competition. The problem setter committee aligned with the mission of AGI Odyssey, which aims to advance innovative research in artificial general intelligence (AGI) and foster interdisciplinary collaboration, and ensure that AGI development benefits humanity as a whole. To maintain the integrity and fairness of the competition, the problem setter committee ensured that all problems were original and kept confidential. Responsibilities of the problem setter committee included problem generation, review, formatting, testing, and revisions for GAIC Math 2024.


A new dataset of 387 questions and solutions from high school competition questions, high school mathematics questions, and university-level mathematics questions.


| ID | ID         | Level                                     | Label                                              | Number   | 
|----|------------|-------------------------------------------|----------------------------------------------------|----------|
| 1  | MIT        | high school competition                   | Algebra                                            | 82       | 
| 2  | MIT        | high school competition                   | NumberTheory                                       | 4        | 
| 3  | MIT        | high school competition                   | Geometry                                           | 25       | 
| 4  | MIT        | high school competition                   | Combinatorics                                      | 37       | 
| 5  | MIT        | high school mathematics questions         | Algebra                                            | 69       | 
| 6  | MIT        | high school mathematics questions         | Geometry                                           | 14       | 
| 7  | MIT        | high school mathematics questions         | PreCalculus                                        | 47       | 
| 8  | MIT        | high school mathematics questions         | Trigonometry                                       | 2        | 
| 9  | MIT        | high school mathematics questions         | Calculus                                           | 5        | 
| 10 | MIT        | high school mathematics questions         | Series                                             | 1        | 
| 11 | MIT        | university-level                          | Linear Algebra and Abstract Algebra                | 25       | 
| 12 | MIT        | university-level                          | Calculus and Analysis                              | 24       | 
| 13 | MIT        | university-level                          | Differential Equations                             | 14       | 
| 14 | MIT        | university-level                          | Probability                                        | 21       | 
| 15 | MIT        | university-level                          | Statistics                                         | 17       | 

## Evaluation Baseline

Evaluation Results of gpt-4-0125-preview on the GAIC Math 2024 problem setter.
![visualize based on different label](./docs/acc_by_label.webp)

![visualize based on different level](./docs/acc_by_level.webp)


## News

🌟 The GAIC competition was scheduled to commence on March 16, 2024, at 12:00 AM US Eastern Standard Time (EST). The competition ended by 11:59 PM US Eastern Standard Time (EST) on March 16, 2024.

## Quick Tour

To duplicate the baseline evaluation result, we provide the tutorials.

The first step is to generate the response using gpt4.
```python
python generate_response.py
```

The second step is to compare with the right answer:
```python
python evaluate_response.py
```


## ​​Acknowledgement

We would like to extend our sincere gratitude to AGI Odyssey, the NGO responsible for organizing the Global Artificial Intelligence Championships (GAIC) Math 2024. Their dedication and commitment to promoting artificial intelligence education and innovation have been invaluable to the success of this project. Additionally, we appreciate their contribution of resources and support, which have played a significant role in making this initiative possible.

## Citation

```latex
@misc{netmindmath,
  author = {Netmind.AI},
  title = {Odyssey-Math},
  year = {2024},
  publisher = {GitHub},
  journal = {GitHub Repository},
  howpublished = {\url{https://github.com/protagolabs/odyssey-math/tree/main}},
  note = {Accessed: April 22, 2024}
}
```
