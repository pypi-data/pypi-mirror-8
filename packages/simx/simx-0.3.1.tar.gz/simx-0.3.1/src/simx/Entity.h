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
// File:    Entity.h
// Module:  simx
// Author:  Lukas Kroc, Sunil Thulasidaasan
// Created: Jan 11 2005
//
// Description:
//	Base class for everything uniquely identifiable (has globally
//	unique ID)
//	Entitites have services, which do most of the work
//
// @@
//
//--------------------------------------------------------------------------

#ifndef NISAC_SIMX_ENTITY
#define NISAC_SIMX_ENTITY

#include "simx/type.h"
#include "simx/Input.h"
#include "simx/Info.h"
#include "simx/InfoRecipient.h"
#include "simx/ExceptionServiceNotFound.h"
//#include "simx/Service.h"

#include "Random/Random.h"

#include "boost/shared_ptr.hpp"
//#include <boost/python.hpp>

#include <map>
#include <list>
#include <utility>

namespace simx {

typedef float Weight;		///< The weight is use to distinguish the difference of different entities

class LP;
class Service;

/// input information for Entity
struct EntityInput : public Input
{
    /// Profile entries
    typedef std::list<ServiceAddress> ServiceAddresses;
    typedef std::pair<ServiceAddresses, ServiceName> ServiceAssignment;
    typedef std::list<ServiceAssignment>	Services;
    Services	fServices;	///< a map of which services should be created on this Entity

    virtual void readProfile(ProfileSource&);
    static void loadServices( EntityInput&, std::string );	///< load services given a string ADDR=SERVICE ...
    virtual void print(std::ostream&) const;

    /// CustomData entries
    // - no custom data entries
};

/// Base class for everything uniquely identifiable (has globally
/// unique ID) Entitites have services, which do most of the work
class Entity
{
    public:
	typedef std::string ClassType;	///< type to use to identify a specific descendant class

   /// creates services on an Entity ent
   /// to be called in a constructor of Entity-derived type after initialization
   static void createServices(Entity& ent, const EntityInput::Services& services);
    
	/// creates an entity on lp and 
	Entity(const EntityID& id, LP& lp, const EntityInput& input);
	virtual ~Entity() = 0;	// the object must be polymorphic

	/// returns ID of the entity
	EntityID getId() const;




	/// returns associated random stream (calls LP::getRandom)
	Random::TRandom& getRandom() const;

	/// returns current simulation time (calls LP::getNow())
	Time getNow() const;

	/// does not actually send an info, but prepares it to  be sent for the 
	/// processOutgoingInfo function
	/// By default, INVALIDATES (reset()) the pointer that it is given!
	/// does NOT copy the Info object, only the pointer
	/// the Info should not be altered after calling this 
	/// (even if another pointer to is exists so that we could)
	///
	/// \param Info to send (WILL BE INVALIDATED by default) must not be NULL
	/// \param Delay after which the Info is delivered (should be >= MINDELAY)
	/// \param Entity to deliver it to
	/// \param Service to deliver it to
	/// \param whether or not to invalidate the pointer (warns if the pointer is not unique and is true) (default true)
	template<typename InfoClass>
	  void sendInfo(boost::shared_ptr<InfoClass>&, const Time&, const EntityID&, const ServiceAddress&, const bool = true) const;


	/// sends an Info
	/// \param Info to send, must not be NULL
	/// \param Delay after which the Info is delivered (should be >= MINDELAY)
	/// \param Entity to deliver it to
	/// \param Service to deliver it to
	virtual void processOutgoingInfo(const boost::shared_ptr<const Info>, const Time&, const EntityID&, const ServiceAddress&) const;

	/// sends an Info to be delivered out-of-band, i.e not a normal event-info
	// will be sent through direct communication between simx layers
	virtual void processOutgoingControlInfo(const boost::shared_ptr<const Info>, const Time&, const EntityID&, const ServiceAddress&) const;

	/// receives an info-receiving and dispatches it to service(s)
	/// if it cannot be delivered to ServiceAdddress (no service at
	/// that address or serviec that cannot handle that info), then outputs
	/// a warning and drops the Info
	virtual void processIncomingInfo(boost::shared_ptr<Info>, const ServiceAddress&) const;

	/// processes an info that was received out-of-band i.e not a normal event-info
	/// but through direct communication between simx layers on distributed processors
        virtual void processIncomingControlInfo( boost::shared_ptr<Info>, const ServiceAddress&) const;


	/// accesor functions to Services, returns false iff the service is not found 
	/// (if the service is not available on the entity) or cannot be interpreted
	/// as the given type
	/// boost::shared_ptr<ServiceClass> is NOT 0 after the call if return value is true
	/// if return value is false, the boost::shared_ptr<> is not modified
	template<class ServiceClass> 
	bool getService(ServiceAddress, boost::shared_ptr<ServiceClass>&) const throw();

	/// set service boost::shared_ptr<Service> to live at ServiceAddress (possibly overwriting
	/// previous service that lives at ServiceAddress)
	/// - if the boost::shared_ptr<> is 0, then erases the service
	void setService(ServiceAddress, const boost::shared_ptr<Service>);
	
	/// puts addresses of all services it holds to "addresses" list
	/// does NOT clear the addresses at first
	void getServiceAddresses(std::list<ServiceAddress>& addresses) const;

	Weight getWeight(void) const;		///< Retrun the weight of the entity

	/// printing function
	virtual void print(std::ostream&) const;

    private:
  EntityID	fId;	///< ID of this entity, maybe not necessary
  
	LP&		fLP;	///< LP on which the entity resides

	Weight		fWeight;   	// To indicate the different weight of the entity, default is set to 1

	/// map for services. boost::shared_ptr<Service> is used instead of Service* so that
	/// when user puts a different service in a address, nothing needs to be
	/// dealocated (the service may and may not be in other address as well)
	typedef std::map<ServiceAddress, boost::shared_ptr<Service> >	ServiceMap;
	ServiceMap	fServices;	///< services that live on this Entity
	
	/// shouldn't be needed, unimplemented
	//Entity(const Entity&);
	Entity& operator=(const Entity&);
};
//                                    Raghupathy Sivakumar
//=======================================================================


template<typename ServiceClass> 
bool Entity::getService(ServiceAddress servAddr, boost::shared_ptr<ServiceClass>& ret) const throw()
{
#ifdef DEBUG
    Logger::debug2() << "Entity " << fId << ": looking for service with Address= " << servAddr << " in map " << fServices << std::endl;
#endif
    ServiceMap::const_iterator iter = fServices.find(servAddr);
    if(iter==fServices.end())
    {
#ifdef DEBUG
    	Logger::debug3() << "Entity " << fId << ": service with address " << servAddr 
	                     << " doesn't exist" << std::endl;
#endif
    	return false;
    }
    else
    {
    	SMART_ASSERT( iter->second )( fServices );
    	boost::shared_ptr<ServiceClass> serv = boost::dynamic_pointer_cast<ServiceClass>(iter->second);
    	if( !serv )
    	{
#ifdef DEBUG
	        Logger::debug3() << "Entity " << fId << ": service of an incorrect type requested at addr=" << servAddr 
				 << ", requested: " << typeid(ServiceClass).name() << std::endl;
#endif
		//commenting below line as it does not compile with clang
		//cannot use typeid on a forward declared class. this is 
		//standards-noncompliant - ST
	//				 << ", resident: " << typeid(*(iter->second)).name() << std::endl;
	        return false;
  	  }

    	ret = serv;
    	SMART_ASSERT( ret );
    	return true;
    }
}


template<typename InfoClass>
void Entity::sendInfo(boost::shared_ptr<InfoClass>& info, const Time& delay, const EntityID& dest, const ServiceAddress& serv, const bool invalidate) const
{
    /// see that we have valid input
    if( !info )
    {
      Logger::error() << "Entity: " << fId
		      << " cannot send NULL info" << std::endl;
      return;
    }
    SMART_ASSERT( info );
    
    /// warn about non-uniqueness of the Info pointer, if not disabled
    if( invalidate && !info.unique() )
    {
      Logger::warn() << "Entity: " << fId
		     << " sending an Info that is not unique " << info << std::endl;
    }
#ifdef DEBUG
    Logger::debug3() << "Entity: " << fId << ","
		     << ": sending Info " << info << std::endl;
#endif
    // send it off, and invalidate if not disabled
    if( invalidate )
    {
      processOutgoingInfo(giveup_smart_ptr(info), delay, dest, serv);
    } else
    {
      processOutgoingInfo(info, delay, dest, serv);
    }
}
//============================================================================================
// various helper functons (not methods of Entity)

/// like Entity::getService, but NEVER returns 0 in boost::shared_ptr<> 
/// it throws ExceptionServiceNotFound if the service is not found or of incorrect type
template<typename ServiceClass>
void getRequiredService(const Entity& ent, const ServiceAddress& servAddr, boost::shared_ptr<ServiceClass>& ret)
    throw(ExceptionServiceNotFound)
{
    /// try to get the service
    bool val = ent.getService(servAddr, ret);

    if( !val )
    {
	/// if you cannot, throw an exception:
	throw ExceptionServiceNotFound(ent.getId(), servAddr, typeid(ServiceClass).name());
    }

    SMART_ASSERT( ret );
}

/// calls "receive" method for all services that can receive the Info
/// (e.i. has receive(boost::shared_ptr<InfoType>) method)
/// all services will receive the same pointer (the boost::shared_ptr<> will NOT the unique)
/// \param entity where the services are
/// \param info to deliver
/// \param service that will be excluded from the delivery (default 0 means exclude nothing)
///	(e.g the one which calls this, to prevent infinite recursion)
/// - returns number of services that the info was delivered to
template<typename InfoType>
int distributeInfo(const Entity& ent, boost::shared_ptr<InfoType> info, const Service* const exclude = 0)
{
    std::list<ServiceAddress> addresses;
    ent.getServiceAddresses( addresses );

    //NOTE: must be to compile, doesn't work to have
    // const InfoRecipient<InfoType>* const in the signature directly
    const InfoRecipient<InfoType>* const ptrExclude = 
	dynamic_cast<const InfoRecipient<InfoType>* const>( exclude );
    if( exclude && !ptrExclude )
    {
	Logger::warn() << "deliverInfoToAllServices: called with 'exlude' that cannot "
	    << "be converted to recipient of " << typeid(InfoType).name() << std::endl;
    }

    int counter = 0;
    for(std::list<ServiceAddress>::const_iterator iter = addresses.begin();
        iter != addresses.end();
        ++iter)
    {
        boost::shared_ptr<InfoRecipient<InfoType> > service;
	if( ent.getService( *iter, service ) )
	{
    	    SMART_ASSERT( service )( *iter )( ent ).msg("Invalid service entry on entity");
	    if( &(*service) == ptrExclude )
	    {
	        /// don't inform it
		continue;
	    }
	    
	    service->receive( info );
	    counter++;
	} // else the service cannot receive the InfoType info
    }

    return counter;
}


//=================================================================================
// printing functions

inline std::ostream& operator<<(std::ostream& os, const Entity& d)
{
    d.print(os);
    return os;
}

inline std::ostream& operator<<(std::ostream& os, const Entity* const d)
{
    if(d) { os << d->getId(); }
    else  { os << "NULL"; }
    return os;
}

} // namespace
#endif 

