// Copyright (c) 2012. Los Alamos National Security, LLC. 

// This material was produced under U.S. Government contract DE-AC52-06NA25396
// for Los Alamos National Laboratory (LANL), which is operated by Los Alamos 
// National Security, LLC for the U.S. Department of Energy. The U.S. Government 
// has rights to use, reproduce, and distribute this software.  

// NEITHER THE GOVERNMENT NOR LOS ALAMOS NATIONAL SECURITY, LLC MAKES ANY WARRANTY, 
// EXPRESS OR IMPLIED, OR ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  
// If software is modified to produce derivative works, such modified software should
// be clearly marked, so as not to confuse it with the version available from LANL.

// Additionally, this library is free software; you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License v 2.1 as published by the 
// Free Software Foundation. Accordingly, this library is distributed in the hope that 
// it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of 
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See LICENSE.txt for more details.

//--------------------------------------------------------------------------
// $Id: fstream.h,v 1.1.1.1 2011/08/18 22:19:46 nsanthi Exp $
//--------------------------------------------------------------------------
// File:    fstream.h
// Module:  File
// Author:  Keith Bisset
// Created: August  8 2003
//
// Description: Modified from boost/filesystem/fstream.hpp.
//
//  Changes involve changing path costructors to string, and throwing exceptions
//  when a file cannot be opened.  Changes fall under the following copyright.
//
// @@
//
//  The original code has the following copyright: (C) Copyright Beman Dawes
//  2002. Permission to copy, use, modify, sell and distribute this software is
//  granted provided this copyright notice appears in all copies. This software
//  is provided "as is" without express or implied warranty, and with no claim
//  as to its suitability for any purpose.  See
//  http://www.boost.org/libs/filesystem for documentation.
//
//--------------------------------------------------------------------------

#ifndef NISAC_FILE_FSTREAM
#define NISAC_FILE_FSTREAM

#include <iosfwd>
#include <fstream>
#include <string>

//--------------------------------------------------------------------------

namespace File {

  template < class charT, class traits = std::char_traits<charT> >
  class basic_filebuf : public std::basic_filebuf<charT,traits>
  {

  public:

    virtual ~basic_filebuf();

    std::basic_filebuf<charT,traits> * open( const std::string& filename,
					     std::ios_base::openmode mode );
  };

  //--------------------------------------------------------------------------

  /// \class ifstream fstream.h "File/fstream.h"
  ///
  /// \brief Extend std::ifstream
  ///
  ///  Add costructors that take a string filename. Throw an exception
  ///  when a file cannot be opened.
  template < class charT, class traits = std::char_traits<charT> >
  class basic_ifstream : public std::basic_ifstream<charT,traits>
  {

  public:

    basic_ifstream();

    explicit basic_ifstream(const std::string& filename,
			    std::ios_base::openmode mode = 
			    std::ios_base::in);

    virtual ~basic_ifstream();

    void open(const std::string& filename,
	      std::ios_base::openmode mode = std::ios_base::in);
  };

  //--------------------------------------------------------------------------

  /// \class ofstream fstream.h "File/fstream.h"
  ///
  /// \brief Extend std::ofstream
  ///
  ///  Add costructors that take a string filename. Throw an exception
  ///  when a file cannot be opened.
 
  template < class charT, class traits = std::char_traits<charT> >
  class basic_ofstream : public std::basic_ofstream<charT,traits>
  {

  public:

    basic_ofstream();
    explicit basic_ofstream(const std::string& filename,
			    std::ios_base::openmode mode =
			    std::ios_base::out);

    virtual ~basic_ofstream();

    void open(const std::string& filename,
	      std::ios_base::openmode mode = std::ios_base::out);
  };

  //--------------------------------------------------------------------------

  /// \class fstream fstream.h "File/fstream.h"
  ///
  /// \brief Extend std::fstream
  ///
  ///  Add costructors that take a string filename. Throw an exception
  ///  when a file cannot be opened.

  template < class charT, class traits = std::char_traits<charT> >
  class basic_fstream : public std::basic_fstream<charT,traits>
  {

  public:

    basic_fstream();
    explicit basic_fstream(const std::string& filename,
			   std::ios_base::openmode mode =
			   std::ios_base::in | std::ios_base::out );
    virtual ~basic_fstream();

    void open(const std::string& filename,
	      std::ios_base::openmode mode =
	      std::ios_base::in|std::ios_base::out);
  };

  //--------------------------------------------------------------------------

  typedef basic_filebuf<char> filebuf;

  /// Extension of std::ifsteam
  typedef basic_ifstream<char> ifstream;

  /// Extension of std::ofsteam
  typedef basic_ofstream<char> ofstream;

  /// Extension of std::fsteam
  typedef basic_fstream<char> fstream;
} // namespace

//--------------------------------------------------------------------------
#endif // NISAC_FILE_FSTREAM
//--------------------------------------------------------------------------
