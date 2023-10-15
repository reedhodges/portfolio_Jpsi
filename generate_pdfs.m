(* ::Package:: *)

(* ::Text:: *)
(*This requires ManeParse and WW-SIDIS to be installed.*)


(* ::Text:: *)
(*https://ncteq.hepforge.org/mma/index.html*)


(* ::Text:: *)
(*https://github.com/prokudin/WW-SIDIS*)


(* ::Input:: *)
(*(* gluon PDF: NNPDF collaboration, via ManeParse *)*)


(* ::Input:: *)
(*gPDF=Flatten[Table[{x,Q,pdfFunction[5,0,x,Q]},{x,0.01,1.0,(1.0-0.01)/200},{Q,5,50,(50.0-5.0)/200}],1]*)


(* ::Input:: *)
(*Export[NotebookDirectory[]<>"pdf_data/gPDF.csv",gPDF]*)


(* ::Input:: *)
(*(* up and down quark PDFs: from WW-SIDIS *)*)


(* ::Input:: *)
(*uPDF=Flatten[Table[{x,Q,f1u[x,Q^2]},{x,0.01,1.0,(1.0-0.01)/200},{Q,5,50,(50.0-5.0)/200}],1]*)


(* ::Input:: *)
(*dPDF=Flatten[Table[{x,Q,f1u[x,Q^2]},{x,0.01,1.0,(1.0-0.01)/200},{Q,5,50,(50.0-5.0)/200}],1]*)


(* ::Input:: *)
(*Export[NotebookDirectory[]<>"pdf_data/uPDF.csv",uPDF]*)


(* ::Input:: *)
(*Export[NotebookDirectory[]<>"pdf_data/dPDF.csv",dPDF]*)
