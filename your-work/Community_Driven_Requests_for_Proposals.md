# COMMUNITY DRIVEN REQUESTS FOR PROPOSALS Applying Semantics to match Customer Purchase Intents to Vendor Offers 

#### Christophe Debruyne 

Semantics Technology and Applications Research Lab, Vrije Universiteit Brussel, Pleinlaan 2, B-1050 Brussels, Belgium christophe.debruyne@vub.ac.be 

#### Davor Meersman 

Digital Ecosystems and Business Intelligence Institute, Curtin University, GPO Box U1987, Perth, WA, 6845, Australia davor.meersman@cbs.curtin.edu.au 

#### Mathias Baert, Rami Hansenne 

iChoosr BVBA, Bourlastraat 3 bus 14, B-2000 Antwerpen, Belgium info@ichoosr.com 

Keywords: 

Product and RFP Ontology, Request for Proposals, Semantic Matching, Data Integration 

Abstract: This paper presents a platform for requests for proposals and describes how ontologies drive the different components: the creation of a proposal, the annotation of vendor data, the transformation of vendor data into other formats and the semantic matching of a proposal against annotated vendor data. The ontology construction started from DOGMA, a methodology with its grounding in the linguistic representation of knowledge that is suitable for community participation in the creation process. The ontologies were created in a modular way, with general product and meta-models that can be extended depending on the domain. In the case of the pilot, the product were holiday packages, more precisely winter sports holiday packages. 

## 1 INTRODUCTION 

When consumers want to buy a certain item on the World Wide Web today, they have to browse through literally hundreds of offerings and results and this number is expected to increase in the future. In this model, the vendors drive the process by publishing products and providing means to buy these online. For example, travel agencies in the Netherlands need to query many different tour operators to find holiday packages meeting their customers’ requirements. They often have an API that facilitates this process, but the granularity of the specific search is often limited due to the heterogeneous nature of all vendor databases. 

A solution to this problem would be to allow the consumers to specify their requirements and to match these to offers of different vendors. Such a specification is called a Request for Proposals (RFP). The COMDRIVE RFP project resulted in a platform enabling consumers to drive the requirements process by expressing their intent to buy a certain product in a tool and language they are comfortable with. This platform sends out the request to a distributed vendor infrastructure, which responds to the request with offers. 

The RFP, the heterogeneous vendor data, the 

matching of both and an appropriate interface for the customer all need to be driven by a agreed upon conceptual model, called an ontology. An ontology is commonly defined as: “a [formal,] explicit specification of a [shared] conceptualization” (Gruber, 1995) and are now key to enable semantic interoperability between information systems and services on the Web (Guarino, 1998). In general, interoperability is defined as the ability of two or more information systems or their (computerized) components to exchange data, knowledge or resources and to interpret the information in them (De Leenheer and Mens, 2008), in this case the RFP platform and the different vendor applications. 

This paper presents the platform and how ontologies and semantic technology are key in achieving success. The content of this paper is organized as follows: Section 2 provides more context about the project and the motivation why such a portal should be driven by ontologies. Section 3 presents the ontology engineering methodology adopted and applied within the project as well as how the resulting ontologies were applied to achieve the platform’s tasks. Section 4 provides some preliminary results during the pilot before concluding and discussion our work in Section 5. Throughout this paper, the examples used stem from the domain of winter holiday packages (in- 

cluding winter sports, accommodation, facilities). 

## 2 CONTEXT AND PROBLEM 

iChoosr BVBA<sup>1</sup> is an internet company who specializes in supporting communities in organizing group buying events (GBE) in spirit of Vendor Relationship Management (VRM). VRM means providing customers with tools for engaging with vendors in ways that work for both parties, as it is difficult for vendors to fully relate with customers. These GBEs gives customers significant volume discounts. In return, iChoosr supports vendors in finding the appropriate customers, who also diminish their costs in logistics. A GBE always consists of a community identified by a particular need for a product (e.g., heating oil) who is represented by a community leader. 

Milq Media<sup>2</sup> is the publisher of the wintersporters.nl/ platform and agreed to take part as pilot partner in this project. Wintersporters.nl’s content is characterized by its actuality and a large amount of objective information. With an average reach of more than 600.000 visitors per month, it is the largest winter sports platform in The Netherlands. The community of wintersporters.nl, with Milq Media acting as the community leader, was therefore chosen to be the pilot partner within this project. 

The pilot of the platform consists of a personal RFP for travel in cooperation with the publisher of online travel platforms Milq Media. During this pilot, members of the Milq Media user community can set out Personal RFPs with the system and get offers from interested travel vendors. The matching engine automatically found some of these offers; other offers were matched manually by an employee of a travel vendor. The user and the vendor can also communicate through a message system. This allows them to further clarify the request and the offer. 

The main components of this platform are: 

- Personal RFP Ontology. A semantic and extensible conceptualization of RFP. An ontology that describes the domain-specific Personal RFPs, allowing communities to contribute product- and domain specific concepts through collaborative knowledge engineering. 

- An Automated Group Buying (AGB) module that allows community leaders to organize their group buying activities online with their community members with support for member group buying process initiation. 

- 1http://www.ichoosr.com/ 

- 2http://www.milq.nl/ 

- Semantic Matching Engine. Matching of customer intent and vendor offering based on shared, personal customer purchasing profile and community profile for accurate offerings based on predefined and implicit criteria. Matching of semantic product data and flat vendor data annotated with the ontology. 

- Rapid Semantic Node Cloud Navigation. Dynamic node cloud underpinned by semantic product data for rapid navigation through correlated product concepts. Combines the ease of use of tag clouds with the ability to process structured data. 



<!-- Start of picture text -->
COMDRIVE RFP Platform<br>Result matches<br>Consumer PortalPortal Matcher<br>commits to Uses<br>Ontology<br>Requests<br>commits to commits to commits to commits to<br><!-- End of picture text -->



<!-- Start of picture text -->
request<br>offer<br><!-- End of picture text -->



<!-- Start of picture text -->
Consumer PortalPortal<br>request<br>offer<br><!-- End of picture text -->





<!-- Start of picture text -->
Vendor applications/databases<br><!-- End of picture text -->



<!-- Start of picture text -->
Vendor applications/databases<br><!-- End of picture text -->



Figure 1: COMDRIVE RFP: The role of semantics in the annotation of vendor data and customer intent for semantic matching. 

For this solution to be truly effective, buyers and vendors need to share a common vocabulary of the domain. More specifically, software agents need to interpret the information in RFPs to (semi-) automatically match this information with data in the vendors’ product database based on their semantics. The semantic of the domain is provided by its conceptualization, which enables the alignment of the vendors’ and buyers’ perspectives. A conceptualization provides a shared agreement on the semantics of core concepts and the relationships between them imposing a structure on the domain that is readable by both humans and machines. In COMDRIVE RFP, the personal RFP ontology is thus key in the other modules’ functioning. 

## 3 APPROACH 

The creation and application of ontologies within COMDRIVE RFP were constructed in an iterative manner. This section explains how the ontologies came to be and were then used to annotate vendor 

data, which were in turn used by the semantic matching to transform that data in a internal format suitable for the task. 

### 3.1 Ontology Engineering Methodology 

Many collaborative ontology engineering methodologies exists (Sure et al., 2009). We adopted DOGMA (Jarrar and Meersman, 2009), which stands out for its groundings in linguistics. DOGMA relies on the fact that its knowledge building blocks expressed in natural language are easily obtained and agreed upon (as inspired by database modeling methodologies such as NIAM (Wintraecken, 1990) and ORM (Halpin, 2008)). As a result, domain experts and knowledge engineers can use natural language to communicate and capture knowledge. 

These building blocks - called lexons (Jarrar and Meersman, 2009) - only need in principle to express “plausible” facts (as perceived by the community of stakeholders) in order to be entered into the Lexon Base, a repository containing large sets of such lexons. A lexon is formally described as a 5-tuple ⟨γ, headterm, role, co-role, tailterm ⟩, where γ is an abstract context identifier pointing to a resource (e.g., a document on the Web). The context identifier is assumed to identify unambiguously (to human users at least) the concepts denoted by the term and role labels. Figure 3 shows some examples of lexons. 

The Commitment Layer contains selections of lexons to annotate (types of) applications and constraints rules defining the use of the concepts in the ontology. In DOGMA, we distinguish two types of commitments: ontologies and application commitments. The first denotes a meaningful selection of lexons and rules that capture well the intended semantics of an application domain. The latter extends the community commitments mappings describing how the application symbols (e.g., fields in a table) of one individual application map to concepts in the ontology. The application commitment can furthermore contain additional lexons and constraints that describe how the application - as a whole - commits to the ontology. Section 3.2 and 3.3 discusses respectively the 

### 3.2 Ontology Construction 

Before building an ontology from scratch, one has to look around for existing meta-models. With metamodel, we mean any kind of conceptual model, not necessarily implemented with semantic technology (such as XML Schemas, or a code-based classification). (Hepp et al., 2007) analyzed and compared 



<!-- Start of picture text -->
Lexons<br>Ontologies<br>Application Mapping 1 ... Application Mapping N CommitmentsApplication<br><!-- End of picture text -->

Figure 2: The different layers in DOGMA. Lexons in the Lexon Base are used to construct ontologies (with additional) constraints. Application commitments extends those ontologies with mappings of application symbols to the ontology. 

four important product meta-models: eCl@ss<sup>3</sup> , UNSPSC<sup>4</sup> , EOTD<sup>5</sup> and RosettaNet Technical Dictionary<sup>6</sup> . Both eCl@ss and UNSPSC are broad, but the first was were created by and driven by the German industry and thus a “de facto standard”, whereas the latter was driven by the United Nations Development Programme. Both UNSPSC and eCl@ss provide very little detail for the traveling domain. The others were designed for more technical industries and did not fit the scope of this project. 

Travel meta-models include Hi-Touch<sup>7</sup> , OnTour<sup>8</sup> , Harmonise (Dell’Erba et al., 2002) and the Open Travel Alliance (OTA) specification<sup>9</sup> . Harmonise focuses on accommodation and events (e.g., sports and conferences), but its main aim is to transfer data between tourism industry partners. Hi-Touch is a thesaurus implemented in OWL to align different vendor databases, but is a commercial product. OnTour, a recent initiative, mainly covers accommodation and activities. OTA provides a structure for electronic messages, e.g., concerning flights, insurance, etc. Hi-touch and OnTour ontologies were developed based on international standards whereas OTA and Harmonise provide their own standards. We drew inspiration from these meta-models to bootstrap an initial product ontology. 

By our knowledge, no RFP meta-model exists. GoodRelations (Hepp, 2008) is a lightweight ontology to annotate most aspects of offers and their goods on the Web. Not exactly modeling an RFP, GoodRelations captures nicely what could be returned as a response or compared with a customer’s 

3http://www.eclass-online.com/ 4http://www.unspsc.org/ 

5http://www.eccma.org/ 6http://www.rosettanet.org/ 

7http://www.mondeca.com/ 

8http://e-tourism.deri.at/ont/index.html 

9http://www.opentravel.org/ 





<!-- Start of picture text -->
provided by/ provides<br>has/ of<br>provided by/ provides<br><!-- End of picture text -->



<!-- Start of picture text -->
DEVindVAKANTIEZOEKER jouw ideale wintervakantie wintersporters.n|. e<br>@ Jouw zoekopdracht Zet ons aan het werk Bevestiging<br>de zoekt Jouw zoekopdracht  Voeg nog enkele criteria toe zoals bestemming,<br>— 5 aantal personen en vertrekdatum<br>[ima [spiel]<br>[Aantal pervonen | Skigebied ares<br>|toegelaten...Sauna, Huisdieren Zoeken<br>Feuerkogel Annuleren<br><!-- End of picture text -->

map "/matchObjects/matchObject/numericalMatchProperty[@id=’Value of Price of Holiday Package’]/value" on Value of Price of Holiday Package. 

map "/matchObjects/matchObject/stringMatchProperty[@id=’Currency of Price of Holiday Package’]/value" on Currency of Price of Holiday Package. 

Figure 8: Mapping the application symbols to lexons 

tent and what is offered by vendors (e.g., “distance to the lift”). We have seen that merely building ontologies on top of the data that is provided by vendors does not solve the problem of finding products that match user needs. When given the liberty of defining ones wish, users demonstrate the desire to involve information that pertains to the product application domain. Although some of these concepts were present in the ontology, there was no data to work with. 

## 5 CONCLUSIONS 

This paper presented the COMDRIVE RFP platform that enables customers to define purchase intent, called an RFP, which can then be matched against annotated vendor data. All modules (RFP creation, vendor data annotation and transformation, semantic matching) are driven by an ontology with different layers of abstraction (a general RFP and product ontology and extensions for particular domains). The method for ontology creation was based on linguistics, which facilitated the dialogue with the different domain experts. 

Future work includes the application of the upper common ontologies (RFP, and product) in other domains for validation and refinement as well as the application of the domain application ontology to other types of holiday packages (e.g., camping). In the future, a more prominent role for community aspects will be investigated. These can be useful to provide even better matching results, as different communities behave differently (e.g., younger people tend to put more emphasis on budget constraints). 

## ACKNOWLEDGEMENTS 

The results of this research were partially funded by IWT<sup>12</sup> 090214 SME innovation project “COMDRIVE RFP”. We also would like to thank Quentin Reul, Maarten Smolders, Tanguy Coenen for the fruitful discussions. 

12http://www.iwt.be/ 

## REFERENCES 

- De Leenheer, P. and Mens, T. (2008). Ontology evolution. In Hepp, M., De Leenheer, P., de Moor, A., and Sure, Y., editors, Ontology Management, volume 7 of Semantic Web And Beyond Computing for Human Experience, pages 131–176. Springer. 

- Dell’Erba, M., Fodor, O., Ricci, F., and Werthner, H. (2002). Harmonise: A solution for data interoperability. In Monteiro, J. L., Swatman, P. M. C., and Valadares Tavares, L., editors, I3E, volume 233 of IFIP Conference Proceedings, pages 433–445. Kluwer. 

- Gruber, T. R. (1995). Toward principles of the design of ontologies used for knowledge sharing. International Journal of Human and Computer Studies, 43:907– 928. 

- Guarino, N. (1998). Formal ontology and information systems. In Int. Conference On Formal Ontology In Information Systems FOIS’98, pages 3–15, Trento, Italy. Amsterdam, IOS Press. 

- Halpin, T. (2008). Information Modeling and Relational Databases. Morgan Kaufmann, San Francisco, CA, USA. 

- Hepp, M. (2008). GoodRelations: An ontology for describing products and services offers on the web. In Gangemi, A. and Euzenat, J., editors, EKAW, volume 5268 of LNCS, pages 329–346. Springer. 

- Hepp, M., Leukel, J., and Schmitz, V. (2007). A quantitative analysis of product categorization standards: content, coverage, and maintenance of eCl@ss, UNSPSC, eOTD, and the RosettaNet Technical Dictionary. Knowledge Information Systems, 13(1):77–114. 

- Jarrar, M. and Meersman, R. (2009). Ontology engineering – the DOGMA approach. In Dillon, T., Chang, E., Meersman, R., and Sycara, K., editors, Advances in Web Semantics I, volume 4891 of LNCS, pages 7–34. Springer Berlin / Heidelberg. 

- Sure, Y., Staab, S., and Studer, R. (2009). Ontology engineering methodology. In Bernus, P., Blazewicz, J., Schmidt, G¨unter, J., Shaw, M. J., Staab, S., and Studer, R., editors, Handbook on Ontologies, International Handbooks on Information Systems, pages 135–152. Springer Berlin Heidelberg. 

- Verheyden, P., De Bo, J., and Meersman, R. (2004). Semantically unlocking database content through ontologybased mediation. In Bussler, C., Tannen, V., and Fundulaki, I., editors, SWDB, volume 3372, pages 109– 126. 

- Wintraecken, J. (1990). The NIAM Information Analysis Method, Theory and Practice. Kluwer Academic Publishers. 

