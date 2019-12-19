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

#ifndef PYTHON_CALLBACK_H
#define PYTHON_CALLBACK_H

#include "ns3/header.h"

namespace ns3 {
/**
 * TODO: Description
 */
class PythonCallback
{
public:
    PythonCallback();
    virtual ~PythonCallback();
    virtual int getData();
    virtual bool isOverridden();
};

} // namespace ns3

#endif /* PYTHON_CALLBACK_H */
