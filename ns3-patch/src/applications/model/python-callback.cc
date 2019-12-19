/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * Copyright 2007 University of Washington
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */
#include "ns3/header.h"
#include "ns3/log.h"
#include "python-callback.h"

namespace ns3 {

NS_LOG_COMPONENT_DEFINE ("PythonCallback");


PythonCallback::PythonCallback ()
{
  NS_LOG_FUNCTION (this);
}


PythonCallback::~PythonCallback()
{
  NS_LOG_FUNCTION (this);
}


int
PythonCallback::getData ()
{
  NS_LOG_FUNCTION (this);
  return 0;
}

bool
PythonCallback::isOverridden ()
{
  NS_LOG_FUNCTION (this);
  return false;
}

} // namespace ns3

