#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 13:53:07 2021

@author: lpellegr
"""
def Card_3_buttons (title, ip, imageurl, calling_id, called_id, parsed_url, peer, button_1, button_1_action, button_2, button_2_action, history, day):
  card_3_buttons = {
    "type": "AdaptiveCard",
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "version": "1.2",
    "body": [
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": title,
                            "wrap": True,
                            "weight": "Lighter",
                            "size": "ExtraLarge"
                        },
                        {
                            "type": "TextBlock",
                            "text": ip,
                            "wrap": True,
                            "size": "ExtraLarge",
                            "weight": "Lighter"
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                        {
                            "type": "ImageSet",
                            "images": [
                                {
                                    "type": "Image",
                                    "size": "Medium",
                                    "url": imageurl
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "type": "TextBlock",
            "text": history,
            "wrap": True,
            "separator": True,
            "size": "Small"
        },
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": "90px",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Calling",
                            "wrap": True,
                            "weight": "Bolder"
                        },
                        {
                            "type": "TextBlock",
                            "text": "Called",
                            "wrap": True,
                            "weight": "Bolder"
                        },
                        {
                            "type": "TextBlock",
                            "text": "Expressway",
                            "wrap": True,
                            "weight": "Bolder"
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": calling_id,
                            "wrap": False
                        },
                        {
                            "type": "TextBlock",
                            "text": called_id,
                            "wrap": False
                        },
                        {
                            "type": "TextBlock",
                            "text": peer,
                            "wrap": False
                        }
                    ]
                }
            ]
        },
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                        {
                            "type": "ActionSet",
                            "actions": [
                                {
                                    "type": "Action.Submit",
                                    "title": button_1,
                                    "data": {
                                            "callback_keyword": "callback___exempt",
                                                                "action": button_1_action,
                                                                "IP": ip,
                                                                "expe": parsed_url,
                                                                "peer": peer,
                                                                "time": day
                                                                }
                                }
                            ],  
                            "isVisible": True,
                            "horizontalAlignment": "Center"
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                        {
                            "type": "ActionSet",
                            "actions": [
                                {
                                    "type": "Action.Submit",
                                    "title": button_2,
                                    "data": {
                                            "callback_keyword": "callback___exempt",
					                        "action": button_2_action,
					                        "IP": ip,
					                        "expe": parsed_url,
					                        "peer": peer,
                                            "time": day
                                                                }

                                }
                            ],
                            "isVisible": True,
                            "horizontalAlignment": "Center"
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                        {
                            "type": "ActionSet",
                            "actions": [
                                {
                                    "type": "Action.Submit",
                                    "title": "More Info",
                                    "data": {
                                        "callback_keyword": "callback___sendfile",
                                        "action": "sendfile",
                                        "IP": ip,
                                        "expe": parsed_url
                                    }
                                }
                            ],
                            "horizontalAlignment": "Center"
                        }
                    ]
                }
            ]
        }
    ]
  }
  return card_3_buttons

def Card_2_buttons (title, ip, imageurl, calling_id, called_id, parsed_url, peer, button_1, button_1_action, history, day):
      card_2_buttons = {
          "type": "AdaptiveCard",
          "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
          "version": "1.2",
          "body": [
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": title,
                            "wrap": True,
                            "weight": "Lighter",
                            "size": "ExtraLarge"
                        },
                        {
                            "type": "TextBlock",
                            "text": ip,
                            "wrap": True,
                            "size": "ExtraLarge",
                            "weight": "Lighter"
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                        {
                            "type": "ImageSet",
                            "images": [
                                {
                                    "type": "Image",
                                    "size": "Medium",
                                    "url": imageurl
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "type": "TextBlock",
            "text": history,
            "wrap": True,
            "separator": True,
            "size": "Small"
        },
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": "90px",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Calling",
                            "wrap": True,
                            "weight": "Bolder"
                        },
                        {
                            "type": "TextBlock",
                            "text": "Called",
                            "wrap": True,
                            "weight": "Bolder"
                        },
                        {
                            "type": "TextBlock",
                            "text": "Expressway",
                            "wrap": True,
                            "weight": "Bolder"
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": calling_id,
                            "wrap": False
                        },
                        {
                            "type": "TextBlock",
                            "text": called_id,
                            "wrap": False
                        },
                        {
                            "type": "TextBlock",
                            "text": peer,
                            "wrap": False
                        }
                    ]
                }
            ]
        },
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                        {
                            "type": "ActionSet",
                            "actions": [
                                {
                                    "type": "Action.Submit",
                                    "title": button_1,
                                    "data": {
                                            "callback_keyword": "callback___exempt",
                                                                "action": button_1_action,
                                                                "IP": ip,
                                                                "expe": parsed_url,
                                                                "peer": peer,
                                                                "time": day
                                                                }
                                }
                            ],  
                            "isVisible": True,
                            "horizontalAlignment": "Center"
                        }
                    ]
                },
                
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                        {
                            "type": "ActionSet",
                            "actions": [
                                {
                                    "type": "Action.Submit",
                                    "title": "More Info",
                                    "data": {
                                        "callback_keyword": "callback___sendfile",
                                        "action": "sendfile",
                                        "IP": ip,
                                        "expe": parsed_url
                                    }
                                }
                            ],
                            "horizontalAlignment": "Center"
                        }
                    ]
                }
            ]
        }
    ]
  }
      return card_2_buttons
