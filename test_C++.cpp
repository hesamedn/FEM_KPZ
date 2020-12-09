#include <iostream>
#include <vector>

template<typename T>
std::vector<double> linspace(T start_in, T end_in, int num_in)
{

  std::vector<double> linspaced;

  double start = static_cast<double>(start_in);
  double end = static_cast<double>(end_in);
  double num = static_cast<double>(num_in);

  if (num == 0) { return linspaced; }
  if (num == 1) 
    {
      linspaced.push_back(start);
      return linspaced;
    }

  double delta = (end - start) / (num - 1);

  for(int i=0; i < num-1; ++i)
    {
      linspaced.push_back(start + delta * i);
    }
  linspaced.push_back(end); // I want to ensure that start and end
                            // are exactly the same as the input
  return linspaced;
}

void print_vector(std::vector<double> vec)
{
  std::cout << "size: " << vec.size() << std::endl;
  for (double d : vec)
    std::cout << d << " ";
  std::cout << std::endl;
}

int main()
{
  std::vector<double> vec_1 = linspace(1, 10, 3);
  print_vector(vec_1);

  std::vector<double> vec_2 = linspace(6.0, 23.4, 5);
  print_vector(vec_2);

  std::vector<double> vec_3 = linspace(0.0, 2.0, 1);
  print_vector(vec_3);

  std::vector<double> vec_4 = linspace(0.0, 2.0, 0);
  print_vector(vec_4);


  return 0;
}