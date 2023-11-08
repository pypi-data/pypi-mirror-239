import pathlib
import unittest
import asyncio
from unittest.mock import patch, AsyncMock
from pprint import pprint


from patent_chart import parser
from patent_chart import generator

class TestParser(unittest.TestCase):
    package_dir = pathlib.Path(__file__).parents[1]
    patent_257_path = package_dir / 'test_data/US 6,484,257.pdf'
    patent_131_path = package_dir / 'test_data/US 7,600,131.pdf'
    patent_479_path = package_dir / 'test_data/US 5,870,479.pdf'
    patent_448_path = package_dir / 'test_data/US7069448.pdf'
    patent_449_path = package_dir / 'test_data/7069449.pdf'
    patent_application_path = package_dir / 'test_data/US20210365512A1.pdf'
    
    def test_parse_patent_from_pdf_path(self):
        text_lines = parser.parse_text_lines_from_pdf_path(self.patent_257_path)
        parsed_patent = parser.parse_patent_from_text_lines(text_lines)
        # print(parser.group_parsed_patent_by_page(parsed_patent)[23].column_1)
        # return
        self.assertEqual(
            parsed_patent.unique_id,
            parser.PatentUniqueID(
                patent_number='6484257',
                country_code='US',
                kind_code='B1',
            )
        )
        self.assertEqual(
            parsed_patent.beginning_of_specification,
            16
        )
        # claims = parser.parse_claims_from_parsed_patent(parsed_patent)
        # for claim in claims.claims:
        #     print(parser.serialize_claim(claim))
        # return
        # pprint(claims)
        self.assertEqual(
            parsed_patent.beginning_of_claims,
            parser.BeginningOfClaims(
                page_index=23,
                col_index=0,
                line_index=16,
            )
        )
        self.assertEqual(
            parsed_patent.end_of_claims,
            parser.EndOfClaims(
                page_index=23,
                col_index=1,
                line_index=74,
            )
        )

        text_lines = parser.parse_text_lines_from_pdf_path(self.patent_131_path)
        parsed_patent = parser.parse_patent_from_text_lines(text_lines)
        self.assertEqual(
            parsed_patent.unique_id,
            parser.PatentUniqueID(
                patent_number='7600131',
                country_code='US',
                kind_code='B1',
            )
        )
        self.assertEqual(
            parsed_patent.beginning_of_specification,
            12
        )
        self.assertEqual(
            parsed_patent.beginning_of_claims,
            parser.BeginningOfClaims(
                page_index=22,
                col_index=0,
                line_index=11,
            )
        )
        self.assertEqual(
            parsed_patent.end_of_claims,
            parser.EndOfClaims(
                page_index=22,
                col_index=1,
                line_index=42,
            )
        )

        text_lines = parser.parse_text_lines_from_pdf_path(self.patent_479_path)
        parsed_patent = parser.parse_patent_from_text_lines(text_lines)
        self.assertEqual(
            parsed_patent.unique_id,
            parser.PatentUniqueID(
                patent_number='5870479',
                country_code='US',
                kind_code='A',
            )
        )
        self.assertEqual(
            parsed_patent.beginning_of_specification,
            4
        )
        self.assertEqual(
            parsed_patent.beginning_of_claims,
            parser.BeginningOfClaims(
                page_index=7,
                col_index=0,
                line_index=8,
            )
        )
        self.assertEqual(
            parsed_patent.end_of_claims,
            parser.EndOfClaims(
                page_index=7,
                col_index=1,
                line_index=50,
            )
        )

        text_lines = parser.parse_text_lines_from_pdf_path(self.patent_application_path)
        parsed_patent = parser.parse_patent_from_text_lines(text_lines)
        self.assertEqual(
            parsed_patent.unique_id,
            parser.PatentUniqueID(
                patent_number='20210365512',
                country_code='US',
                kind_code='A1',
            )
        )

        self.assertEqual(
            parsed_patent.beginning_of_specification,
            15
        )

        # # TODO: doesn't work yet searching for specific prefatory language because there is none in this case. Would have to have some model to catch this one. Could count number of 'X.' bigrams on page, could use simple naive bayes model, could even just ask LLM.
        # self.assertEqual(
        #     parsed_patent.beginning_of_claims,
        #     parser.BeginningOfClaims(
        #         page_index=22,
        #         col_index=0,
        #         line_index=0,
        #     )
        # )
        # # TODO: doesn't work for this one either
        # self.assertEqual(
        #     parsed_patent.end_of_claims,
        #     parser.EndOfClaims(
        #         page_index=24,
        #         col_index=1,
        #         line_index=0,
        #     )
        # )

        parsed_patent = parser.parse_patent_from_pdf_path(self.patent_448_path)
        self.assertEqual(
            parsed_patent.unique_id,
            parser.PatentUniqueID(
                patent_number='7069448',
                country_code='US',
                kind_code='B2',
            )
        )
        self.assertEqual(
            parsed_patent.beginning_of_specification,
            4
        )
        self.assertEqual(
            parsed_patent.beginning_of_claims,
            parser.BeginningOfClaims(
                page_index=6,
                col_index=1,
                line_index=25,
            )
        )
        self.assertEqual(
            parsed_patent.end_of_claims,
            parser.EndOfClaims(
                page_index=7,
                col_index=1,
                line_index=23,
            )
        )

        # TODO: doesnt work because each page of 449 is a figure. None of the text is selectable. Each page contains a pdfminer.six LTFigure object, which might be an embedded pdf. see comment in pdfminer.six/pdfminer/layout.py: class LTFigure(LTLayoutContainer):
        """Represents an area used by PDF Form objects.

        PDF Forms can be used to present figures or pictures by embedding yet
        another PDF document within a page. Note that LTFigure objects can appear
        recursively.
        """
        # So we might just need to recurse through LTFigure objects when we encounter them as the page contents.
        # parsed_patent = parser.parse_patent_from_pdf_path(self.patent_449_path)

        # TODO: test specific expected lines

    def test_parse_claims_from_parsed_patent(self):
        parsed_patent = parser.parse_patent_from_pdf_path(self.patent_257_path)
        claims = parser.parse_claims_from_parsed_patent(parsed_patent)
        first_claim = parser.serialize_claim(claims.claims[0])
        self.assertEqual(
            first_claim,
            "1. A software architecture for conducting a plurality of 15cryptographic sessions over a distributed computingenvironment, comprising:a registration entity or registry residing within a mamserver entity;an agent server entity communicating with said mam 20server;a client entity communicating with said main server andagent server;a plurality of distributed networked computers providinga mechanism for executing said main server entity,agent server entity, and client entity;a defined protocol for initiating secure communicationbetween the main server and agent server; over saidnetwork; anda system for providing one or more communicationsessions among the main server, agent server and cliententity for implementing a client decrypted bandwidthreconstitution which enables the recombination of individual parts of the decrypted client bandwidth among Nagents processing in parallel."
        )

        claim_elements = parser.serialize_claim_elements(claims.claims[0])
        # TODO: see 'over said network;' parsed as it's own element. Apparently can't rely on ';' separating claim elements in every case.
        self.assertEqual(
            claim_elements,
            ['1. A software architecture for conducting a plurality of 15cryptographic sessions over a distributed computingenvironment, comprising:', 'a registration entity or registry residing within a mamserver entity;', 'an agent server entity communicating with said mam 20server;', 'a client entity communicating with said main server andagent server;', 'a plurality of distributed networked computers providinga mechanism for executing said main server entity,agent server entity, and client entity;', 'a defined protocol for initiating secure communicationbetween the main server and agent server;', 'over saidnetwork;', 'anda system for providing one or more communicationsessions among the main server, agent server and cliententity for implementing a client decrypted bandwidthreconstitution which enables the recombination of individual parts of the decrypted client bandwidth among Nagents processing in parallel.']
        )

        parsed_patent = parser.parse_patent_from_pdf_path(self.patent_448_path)
        claims = parser.parse_claims_from_parsed_patent(parsed_patent)
        
        serialized_claim_1 = parser.serialize_claim_elements(claims.claims[0])
        self.assertEqual(
            serialized_claim_1,
            ['1. A system for cryptographic processing of input data ona parallel processor array that includes a plurality of processors, comprising:', 'a format filter adapted to extract control data and maindata from the input data;', 'a control unit adapted to receive the control data from saidformat filter, and to forward, based at least in part on thecontrol data, at least one respective control parameterand at least one respective cryptographic parameter toeach of the plurality of processors;', 'a first distributor adapted to receive the main data fromsaid format filter, and to distribute to each of theplurality of processors a respective at least a portion ofthe main data;', 'a second distributor adapted to receive respective outputinformation from each of the plurality of processors,and to generate, based at least in part on the respectiveoutput information, output data;', 'wherein each of the plurality of processors is adapted togenerate its respective output information based at leastin part on the control parameters and the cryptographicparameters, and the output data is a cryptographicprocessing result.']
        )

        parsed_patent = parser.parse_patent_from_pdf_path(self.patent_479_path)
        claims = parser.parse_claims_from_parsed_patent(parsed_patent)
        claim_elements = parser.serialize_claim_elements(claims.claims[-1])
        self.assertEqual(
            claim_elements,
            # TODO: need to fix these floating line number lines that get tacked on (3016 should be 16)
            ['3016. A device for cryptographically processing datapackets, each of the data packets belonging to at least one ofa plurality of channels, the device comprising:', 'identification means for identifying the at least one channel to which a data packet belongs;', 'processing means for cryptographically processing thedata packet, wherein the processing means include afirst processing unit and a second processing unit;', 'memory means for storing information, associated witheach of the plurality of channels, for processing datapackets from each of the plurality a channels;', 'andcontrol means for selecting information associated withthe at least one channel which the data packet wasidentified as belonging to, wherein the control meansare designed to assign, on the basis of the identificationof the data packet, the data packet to one of the first andsecond processing units and to process the data packetwith the aid of the selected information.']
        )

    def test_serialize_specification_from_parsed_patent(self):
        parsed_patent = parser.parse_patent_from_pdf_path(self.patent_257_path)
        specification = parser.serialize_specification_from_parsed_patent(parsed_patent)

        self.assertEqual(
            specification[:13],
            ['1', 'SYSTEM AND METHOD FOR MAINTAINING', 'N NUMBER OF SIMULTANEOUS', 'CRYPTOGRAPHIC SESSIONS USING A', 'DISTRIBUTED COMPUTING', 'ENVIRONMENT', 'FIELD OF THE INVENTION', 'The field of the present invention relates generally to the', 'encryption and decryption of data conducted over a distrib', 'uted computer network. In particular, the field of the inven', 'tion relates to a software architecture for conducting a', 'plurality of cryptographic sessions managed over a distrib', 'uted computing environment.']
        )

        parsed_patent = parser.parse_patent_from_pdf_path(self.patent_131_path)
        specification = parser.serialize_specification_from_parsed_patent(parsed_patent)
        self.assertEqual(
            specification[-1],
            'claims and their full scope of equivalents.'
        )

class TestAsyncGenerator(unittest.IsolatedAsyncioTestCase):
    package_dir = pathlib.Path(__file__).parents[1]
    patent_448_path = package_dir / 'test_data/US7069448.pdf'
    patent_131_path = package_dir / 'test_data/US 7,600,131.pdf'
    patent_257_path = package_dir / 'test_data/US 6,484,257.pdf'

    @patch('patent_chart.generator.aopenai_chat_completion_request_with_retry', new_callable=AsyncMock)
    async def test_async_generate(self, mock_aopenai_chat_completion_request_with_retry):
        mock_aopenai_chat_completion_request_with_retry.return_value = ({
            'choices': [
                {
                    'message': {
                        'content': 'generated_passage'
                    },
                }
            ]
        })
        parsed_patent_448 = parser.parse_patent_from_pdf_path(self.patent_448_path)
        parsed_patent_131 = parser.parse_patent_from_pdf_path(self.patent_131_path)
        parsed_patent_257 = parser.parse_patent_from_pdf_path(self.patent_257_path)

        claims_448 = parser.parse_claims_from_parsed_patent(parsed_patent_448)
        
        serialized_claim_elements = []
        for claim in claims_448.claims:
            serialized_claim_elements.extend(parser.serialize_claim_elements(claim))

        generated_passages = set()
        async for generated_passage in generator.abulk_generate_passages(
            (1, parsed_patent_448),
            [(1, parsed_patent_131), (2, parsed_patent_257)],
            [(i, serialized_claim_elements) for i in range(len(serialized_claim_elements))],
        ):
            generated_passages.add(
                (generated_passage.claim_element_id, generated_passage.prior_art_source_id)
            )
        
        self.assertEqual(
            len(generated_passages),
            2 * len(serialized_claim_elements)
        )

        self.assertEqual(
            generated_passages,
            set(
                [
                    (j, i) for i in range(1, 3) for j in range(len(serialized_claim_elements))
                ]
            )
        )