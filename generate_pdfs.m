(* ::Package:: *)

(* This requires ManeParse and WW-SIDIS to be installed. *)
(* https://ncteq.hepforge.org/mma/index.html *)
(* https://github.com/prokudin/WW-SIDIS *)
(* gluon PDF: NNPDF collaboration, via ManeParse *)
gPDF=Flatten[Table[{x,Q,pdfFunction[5,0,x,Q]},{x,0.01,1.0,(1.0-0.01)/200},{Q,5,50,(50.0-5.0)/200}],1]
Export[NotebookDirectory[]<>"pdf_data/gPDF.csv",gPDF]
(* up and down quark PDFs: from WW-SIDIS *)
uPDF=Flatten[Table[{x,Q,f1u[x,Q^2]},{x,0.01,1.0,(1.0-0.01)/200},{Q,5,50,(50.0-5.0)/200}],1]
dPDF=Flatten[Table[{x,Q,f1d[x,Q^2]},{x,0.01,1.0,(1.0-0.01)/200},{Q,5,50,(50.0-5.0)/200}],1]
Export[NotebookDirectory[]<>"pdf_data/uPDF.csv",uPDF]
Export[NotebookDirectory[]<>"pdf_data/dPDF.csv",dPDF]
