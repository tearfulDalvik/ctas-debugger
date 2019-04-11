//
//  forceButton.swift
//  CTAS
//
//  Created by 丰丰哥 on 2018/12/29.
//  Copyright © 2018 丰丰哥. All rights reserved.
//

import AudioToolbox
import UIKit

class ForceButton : UIButton {
    
    override func touchesMoved(_ touches: Set<UITouch>, with event: UIEvent?) {
        for touch in touches {
            if touch.force == touch.maximumPossibleForce {
                let generator = UIImpactFeedbackGenerator(style: .heavy)
                generator.prepare()
                generator.impactOccurred()
            }
        }
    }
}
