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

// $Id$
//--------------------------------------------------------------------------
//
// File:        PyInfo.h
// Module:      Python
// Author:      Sunil Thulasidasan
// Created:     August 3 2012 
// Description: Base class for Infos in Python
//
// @@
//
//--------------------------------------------------------------------------

#ifndef SIMX_PY_INFO_H
#define SIMX_PY_INFO_H


#include "simx/Info.h"
#include <boost/python.hpp>
//#include <boost/serialization/access.hpp>
//#include <boost/make_shared.hpp>
#include "simx/PackedData.h"

//#include <boost/archive/text_iarchive.hpp>;

//#include <boost/archive/text_iarchive.hpp>
namespace simx {

  namespace Python {

    struct PyObjHolder;

    struct PyInfo : public Info {
      
      
      //friend class boost::serialization::access;
      
      //template<class Archive>
      // void serialize(Archive & ar, const unsigned int version)
      // {
      //   ar & fData;
      // }


      PyInfo(); 
      virtual ~PyInfo();
      
      //void readData( Input::DataSource& );

      virtual void pack(simx::PackedData&) const;
      virtual void unpack(simx::PackedData&);

      void readData( const boost::python::object& data);
     
      void setData( const boost::python::object& data);

      const boost::python::object getData() const;

      //boost::shared_ptr<boost::python::object> fData;
      //boost::python::str fPickledData;
      std::string fPickledData;
      bool fPickled;
    private:
      //const boost::python::object* fData;
      //boost::python::object fData2;
      boost::shared_ptr<PyObjHolder> fDataPtr;
      //PyObjHolder* fDataPtr;

    };

 
  } //namespace simx
} // namespace Python


#endif
