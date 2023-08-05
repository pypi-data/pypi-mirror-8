#ifndef __SVM_HPP
#define __SVM_HPP

#include "table.hpp"

#include "classify.hpp"
#include "learn.hpp"
#include "orange.hpp"
#include "domain.hpp"
#include "examplegen.hpp"
#include "table.hpp"
#include "examples.hpp"
#include "distance.hpp"

#include "libsvm/svm.h"

svm_model *svm_load_model_alt(string& buffer);
int svm_save_model_alt(string& buffer, const svm_model *model);

WRAPPER(ExampleGenerator)
WRAPPER(KernelFunc)
WRAPPER(SVMLearner)
WRAPPER(SVMClassifier)
WRAPPER(ExampleTable)

class ORANGE_API TKernelFunc: public TOrange{
public:
	__REGISTER_ABSTRACT_CLASS
	virtual float operator()(const TExample &, const TExample &)=0;
};

WRAPPER(KernelFunc)


class ORANGE_API TSVMLearner : public TLearner{
public:
	__REGISTER_CLASS

  CLASSCONSTANTS(SVMType: C_SVC=C_SVC; Nu_SVC=NU_SVC; OneClass=ONE_CLASS; Epsilon_SVR=EPSILON_SVR; Nu_SVR=NU_SVR)
  CLASSCONSTANTS(Kernel: Linear=LINEAR; Polynomial=POLY; RBF=RBF; Sigmoid=SIGMOID; Custom=PRECOMPUTED)
  CLASSCONSTANTS(LIBSVM_VERSION: VERSION=LIBSVM_VERSION)

	//parameters
	int svm_type; //P(&SVMLearner_SVMType)  SVM type (C_SVC=0, NU_SVC, ONE_CLASS, EPSILON_SVR=3, NU_SVR=4)
	int kernel_type; //P(&SVMLearner_Kernel)  kernel type (LINEAR=0, POLY, RBF, SIGMOID, CUSTOM=4)
	float degree;	//P polynomial kernel degree
	float gamma;	//P poly/rbf/sigm parameter
	float coef0;	//P poly/sigm parameter
	float cache_size; //P cache size in MB
	float eps;	//P stopping criteria
	float C;	//P for C_SVC and C_SVR
	float nu;	//P for NU_SVC and ONE_CLASS
	float p;	//P for C_SVR
	int shrinking;	//P shrinking
	int probability;	//P probability
	bool verbose;		//P verbose

	int nr_weight;		/* for C_SVC */
	int *weight_label;	/* for C_SVC */
	double* weight;		/* for C_SVC */

	PKernelFunc kernelFunc;	//P custom kernel function

	TSVMLearner();
	~TSVMLearner();

	PClassifier operator()(PExampleGenerator, const int & = 0);

protected:
	virtual svm_node* example_to_svm(const TExample &ex, svm_node* node, double last=0.0);
	virtual svm_node* init_problem(svm_problem &problem, PExampleTable examples, int n_elements);
	virtual int getNumOfElements(PExampleGenerator examples);
	virtual TSVMClassifier* createClassifier(
				PDomain domain, svm_model* model, PExampleTable supportVectors, PExampleTable examples);
};

class ORANGE_API TSVMLearnerSparse : public TSVMLearner{
public:
	__REGISTER_CLASS
	bool useNonMeta; //P include non meta attributes in the learning process
protected:
	virtual svm_node* example_to_svm(const TExample &ex, svm_node* node, double last=0.0);
	virtual int getNumOfElements(PExampleGenerator examples);
	virtual TSVMClassifier* createClassifier(
			PDomain domain, svm_model* model, PExampleTable supportVectors, PExampleTable examples);
};


class ORANGE_API TSVMClassifier : public TClassifierFD {
public:
	__REGISTER_CLASS
	TSVMClassifier() {
		this->model = NULL;
	};

	TSVMClassifier(PDomain, svm_model * model, PExampleTable supportVectors,
			PKernelFunc kernelFunc=NULL, PExampleTable examples=NULL);

	~TSVMClassifier();

	TValue operator()(const TExample&);
	PDistribution classDistribution(const TExample &);

	PFloatList getDecisionValues(const TExample &);

	PIntList nSV; //P nSV
	PFloatList rho;	//P rho
	PFloatListList coef; //P coef
	PFloatList probA; //P probA - pairwise probability information
	PFloatList probB; //P probB - pairwise probability information
	PExampleTable supportVectors; //P support vectors

	PExampleTable examples;	//P training instances when svm_type == Custom
	PKernelFunc kernelFunc;	//P custom kernel function used when svm_type == Custom

	int svm_type; //P(&SVMLearner_SVMType)  SVM type (C_SVC=0, NU_SVC, ONE_CLASS, EPSILON_SVR=3, NU_SVR=4)
	int kernel_type; //P(&SVMLearner_Kernel)  kernel type (LINEAR=0, POLY, RBF, SIGMOID, CUSTOM=4)

    svm_model* getModel() {return model;}

protected:
	virtual svm_node* example_to_svm(const TExample &ex, svm_node* node, double last=0.0);
	virtual int getNumOfElements(const TExample& example);

private:
	svm_model *model;
};

class ORANGE_API TSVMClassifierSparse : public TSVMClassifier {
public:
	__REGISTER_CLASS
	TSVMClassifierSparse() {};

	TSVMClassifierSparse(
			PDomain domain, svm_model * model, bool useNonMeta,
			PExampleTable supportVectors,
			PKernelFunc kernelFunc=NULL,
			PExampleTable examples=NULL
			) : TSVMClassifier(domain, model, supportVectors, kernelFunc, examples) {
		this->useNonMeta = useNonMeta;
	}

	bool useNonMeta; //PR include non meta attributes

protected:
	virtual svm_node* example_to_svm(const TExample &ex, svm_node* node, double last=0.0);
	virtual int getNumOfElements(const TExample& example);
};

#endif

