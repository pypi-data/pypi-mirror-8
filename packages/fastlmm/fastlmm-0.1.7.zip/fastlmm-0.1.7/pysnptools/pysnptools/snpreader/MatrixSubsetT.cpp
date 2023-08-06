#include "MatrixSubsetT.h"
#include <iostream>
#include <stdio.h>
#include <math.h> 
#include <stdlib.h>

using namespace std;

void SUFFIX(matrixSubset)(REALIN* in_, int in_iid_count, int in_sid_count, std::vector<size_t> iid_index, std::vector<int> sid_index, REALOUT* out)
{
	//try
	//{

		//std::cout << "in_=" << in_ << ", ";
		//std::cout << "in_iid_count=" << in_iid_count << ", ";
		//std::cout << "in_sid_count=" << in_sid_count << ", ";
		//std::cout << "out=" << out << ", ";
		//std::cout << std::endl;


		uint64_t_ out_iid_count = iid_index.size();
		uint64_t_ out_sid_count = sid_index.size();
		//REALOUT last=0; //!!!cmk

		for (size_t sid_index_out = 0; sid_index_out != out_sid_count; sid_index_out++){


			int sid_index_in = sid_index[sid_index_out];

			REALIN* in2 = in_ + in_iid_count * (uint64_t_) sid_index_in;
			REALOUT* out2 = out + out_iid_count * (uint64_t_) sid_index_out;

			//if (sid_index_out % 100000 == 0 || 567793 == sid_index_out)
			//{
			//	std::cout << "sid_index_out=" << sid_index_out << ", ";
			//	std::cout << "sid_index_in=" << sid_index_in << ", ";
			//	std::cout << "in2=" << in2 << ", ";
			//	std::cout << std::endl;
			//}

			for (size_t iid_index_out = 0; iid_index_out != out_iid_count; iid_index_out++){

				size_t iid_index_in = iid_index[iid_index_out];

				//if (567793 == sid_index_out)
				//{
				//	std::cout << "iid_index_out=" << iid_index_out << ", ";
				//	std::cout << "iid_index_in=" << iid_index_in << ", ";
				//	std::cout << std::endl;
				//}


				out2[iid_index_out] = (REALOUT) in2[iid_index_in];
				//last = in2[iid_index_in]; //!!!cmk

			}
		}
		//std::cout << "last=" << last << std::endl;
	//}
	//catch (const std::exception &exe)
	//{
	//	std::cerr << exe.what();
	//}
}
