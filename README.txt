
-------- -------- AMAZON REVIEWS ANALYSIS -------- -------- 

Corso di Data Analytics a.a. 2018-19
Università degli studi di Milano-Bicocca


-------- Autori

807628  Matteo Basso
807130  Marco Ferri


-------- Struttura progetto

DA-BassoFerri-AmazonReviewsAnalysis-REPORT.pdf	: RELAZIONE PROGETTO
DA-BassoFerri-AmazonReviewsAnalysis-SLIDE.pdf	: PRESENTAZIONE PROGETTO
README.txt					: sono io!

datasets/					: contiene il riferimento al dataset utilizzato 	(capitolo 1.2)
	amazon-5-core.txt			: url del dataset e info aggiuntive sul suo utilizzo
						  una copia del suddetto è reperibile nella cartella scripts/

notebooks/					: Python Jupyter Notebooks
	sentiment.ipynb				: ANALISI ESPLORATIVA, SENTIMENT ANALYSIS E PREDICTION	(capitoli 2, 4 e 5)
	network.ipynb				: NETWORK ANALYSIS e COLLABORATIVE FILTERING		(capitoli 3 e 7)

	Si consiglia l'esecuzione tramite Google Colab per la gestione automatica  delle dipendenze

cytoscape/
	network_analysis.cys			: progetto Cytoscape per la network analysis 	(capitolo 3)
	movielens.cys				: progetto Cytoscape per la rete Movielens 	(capitolo 7.3.2)
	networks/
		clothshoes_full.graphml		: Amazon network
		clothshoes_full.netstats	: Amazon network stats
		movielens.graphml		: Movielens netwok 				(capitolo 7.3.2)
		movielens.netstats		: Movielens network stats 			(capitolo 7.3.2)

scripts/					: Sorgenti Python per ASPECT BASED SENTIMENT ANALYSIS	(capitolo 6)
	requirements.txt			: Lista dipendenze pip
	absa.py					: Effettua l'analisi vera e propria come spiegato in relazione
	aspect_sentiment.py			: Invocato dalla Web demo per utilizzare absa.py
	loadDataset.py				: Invocato dalla Web demo per caricare il dataset
	output.json				: Creato dalla Web demo e letto per la visualizzazione dalla UI
	reviews_Clothing_Shoes[...].gz		: Dataset usato dalla Web demo (equivalente a quello dei notebook)

	È possibile avere una dimostrazione del funzionamento di absa.py con il comando:
	pip install -r requirements.txt
	python aspect_sentiment.py --out myfile.json --threshold 7 --source reviews_Clothing_Shoes_and_Jewelry_5.json.gz

	Qualora non funzionasse, sarebbe richiesta l'installazione di cholmod per l'importazione della libreria nltk
	http://faculty.cse.tamu.edu/davis/suitesparse.html
	https://github.com/jlblancoc/suitesparse-metis-for-windows

app/						: Web demo 					(capitolo 8)
	server/					: Back-end Node.js
	app/					: Front-end React.js

	Previa installazione di Node.js è possibile eseguire la demo tramite i comandi:
	\app\server > npm install
	\app\server > npm start
	\app\client > npm install
	\app\client > npm start
	La demo sarà utilizzabile con un browser all'indirizzo http://localhost:3000/
	(sentiment prediction è da provare in lingua inglese)






