var area = null;
var fighter = null;
var enemy = null;
var bulletNumber = 1;
var fighterGameOver = true;
var fighterSpeed = 1;
var fighterOffset = 1;
var enemySpeed;
var defaultEnemySpeed = 50;
var lockBullet = false;
var fighterScore = 0;
var explosion = false;
var mirageImg = null;
var enemyImg = null;

function removeAt(a, index) {
    if (index > -1) {
        a.splice(index, 1);
    }
}
function normalizeY(obj) {
    var a = new Array();
    
    for(var i = 0; i < obj.pixelsY.length; i ++) {
        a.push(obj.pixelsY[i] + obj.y);
    }
    
    return a;
}

function normalizeX(obj, x) {
    var a = new Array();
    
    for(var i = 0; i < obj.length; i ++) {
        a.push(obj[i] + x);
    }
    
    return a;
}

function collide(obj1, obj2) {
    var a = new Array();
    var b = normalizeY(obj1);
    var c = normalizeY(obj2);
    var f = new Array();
    
    for(var i = 0; i < b.length; i ++) {
        for(var j = 0; j < c.length; j ++) {
            if(b[i] == c[j]) {
                a.push(i);
                f.push(j);
            }
        }
    }
    
    for(var i = 0; i < a.length; i ++) {        
        var d = normalizeX(obj1.pixels[a[i]], obj1.x);
        var e = normalizeX(obj2.pixels[f[i]], obj2.x);

        for(var j = 0; j < d.length; j ++) {
            if($.inArray(d[j], e) != -1) {
                return true;
            }
        }
    }
    
    return false;
}
    
function Bullet(color, x, y, isEnemy) {
    this.PIXEL_COUNT = 10;
    this.bulletInterval = null;
    this.init = init;
    this.fire = fire;
    this.destroy = destroy;
    
    this.color = color;
    this.x = x;
    this.y = y;
    this.isEnemy = isEnemy;
    this.id = 'bullet-' + bulletNumber;
    this.width = 10;
    this.height = 10;
    
    this.init();
    
    function init() {
        this.pixels = new Array();
        this.pixelsY = new Array();
        
        for(var i = 0; i < 10; i ++) {
            this.pixelsY.push(i + 1)
            this.pixels.push(new Array(1, 2, 3, 4, 5, 6, 7, 8, 9, 10));
        }
    }
    
    function fire() {
        var style = 'top: ' + this.y + 'px; left: ' + this.x + 'px;';
        if(this.color != null) {
            style += ' background-color: ' + this.color + ';'
        }
        var cls = this.isEnemy ? 'bullet-enemy' : 'bullet-fighter';
        
        area.append('<div id="' + this.id + '" class="bullet ' + cls + '" style="' + style + '"></div>');
        
        var top = this.isEnemy ? area.height() - 10: 10;
        var plane = this.isEnemy ? fighter: enemy;
        var bullet = this;
        
        $('#' + this.id).animate({
            top: top + 'px'
        }, {
            duration: 3000,
            easing: 'linear',
            step: function(now, fx) {
                if($('#' + bullet.id).length > 0) {
                    var position = $('#' + bullet.id).position();
                    var top = position.top;
                    var left = position.left;
                    
                    top = parseInt(top);
                    
                    bullet.x = left;
                    bullet.y = top;
                    
                    if(bullet.isEnemy) {        
                        for(var j = 0; j < fighter.bullets.length; j ++) {
                            if(collide(bullet, fighter.bullets[j])) {
                                area.append('<div class="bubble bullet-bubble" style="top: ' + bullet.y + 'px; left: ' + bullet.x + 'px;">+ 500</div>');
                                $('.bullet-bubble').fadeOut({duration: 3000});
                                
                                fighterScore += 500;
                                increaseSpeed();
                                $('#fighter-score').html(fighterScore);
                                
                                bullet.destroy();
                                fighter.bullets[j].destroy();
                                
                                var enemyBulletIndex = $.inArray(bullet, enemy.bullets);
                                removeAt(enemy.bullets, enemyBulletIndex);
                                
                                var fighterBulletIndex = $.inArray(fighter.bullets[j], fighter.bullets);
                                removeAt(fighter.bullets, fighterBulletIndex);
                            }
                        }
                    }
                    
                    var obj1 = bullet.isEnemy ? bullet : plane;
                    var obj2 = bullet.isEnemy ? plane : bullet;
                    
                    if(collide(obj1, obj2)) {
                        var bulletIndex = $.inArray(bullet, plane.bullets);
                        removeAt(plane.bullets, bulletIndex);
                        
                        $('#' + bullet.id).remove();
                        if(!plane.isEnemy) {
                            endFighter();
                        } else {
                            fighterScore += 200;
                            increaseSpeed();
                            
                            area.append('<div class="bubble plane-bubble" style="top: ' + plane.y + 'px; left: ' + plane.x + 'px;">+ 200</div>');
                            $('.plane-bubble').fadeOut({duration: 3000});
                                    
                            $('#fighter-score').html(fighterScore);
                            newEnemy();
                        }
                    }
                }
            },
            complete: function() {
                $('#' + bullet.id).remove();
            }
        });
        
        bulletNumber ++;
    }
    
    function destroy() {
        $('#' + this.id).remove();
    }
}

function Mirage(isEnemy) {
    this.PIXEL_COUNT = 224;
    
    this.isEnemy = isEnemy;
    
    this.init = init;
    this.reverse = reverse;
    this.appear = appear;
    this.dissappear = dissappear;
    this.destroy = destroy;
    this.fire = fire;
    this.inBoundsTop = inBoundsTop;
    this.inBoundsLeft = inBoundsLeft;
    this.inBoundsBottom = inBoundsBottom;
    this.inBoundsRight = inBoundsRight;
    this.up = up;
    this.left = left;
    this.down = down;
    this.right = right;
    this.clearMirageInterval = clearMirageInterval;
    
    this.mirageInterval = null;
    
    this.width = 101;
    this.height = 180;
    this.img = mirageImg;
    this.cls = 'mirage';    
    this.bullets = new Array();
    
    this.init();
    
    this.x = Math.floor((Math.random()*(area.width() - this.width * 2)) + 1);
    this.y = area.height() - this.height;
    
    if(this.isEnemy) {
        this.pixels = this.reverse();
        this.y = 0;
        this.img = enemyImg;
        this.cls = 'enemy';
    }
    this.img.css({top: this.y, left: this.x});
    this.img.show();
    area.append(this.img);
    
    this.appear();
    
    function appear() {
        var plane = this;
        
        $('.' + plane.cls).animate({
            opacity: 1
        }, {
            duration: 2000,
            complete: function() {
                if(plane.isEnemy) {
                    plane.fire();
                    plane.clearMirageInterval();
                    plane.mirageInterval = setInterval('enemy.down()', enemySpeed);
                }
            }
        });
    };
    
    function dissappear() {
        var plane = this;
        
        $('.' + this.cls).animate({
            opacity: 0
        }, {
            duration: 2000,
            complete: function() {
                plane.destroy();
                if(!fighterGameOver) {
                    enemy = new Mirage(true);
                }
            }
        });
    };
    
    function fire() {
        var bulletX = this.x + 4;
        var bulletY = this.y + 53;
        var bullet2X = this.x + 88;
        var bullet2Y = this.y + 53;
        
        var color = 'red';
        
        if(!this.isEnemy) {
            color = null;
            bulletX = this.x + 4;
            bulletY = this.y + 118;
            bullet2X = this.x + 88;
            bullet2Y = this.y + 118;
        }
        
        var bullet = new Bullet(color, bulletX, bulletY, this.isEnemy);
        this.bullets.push(bullet);
        bullet.fire();
        
        var bullet2 = new Bullet(color, bullet2X, bullet2Y, this.isEnemy);
        this.bullets.push(bullet2);
        bullet2.fire();
    };
    
    function init() {
        this.pixels = new Array(this.PIXEL_COUNT);
        
        this.pixelsY = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
            31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
            61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 89, 90, 91, 92,
            93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121,
            122, 123, 124, 125, 126, 127, 128, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147,
            148, 149, 150, 151, 152, 153, 154, 155, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156,
            157, 157, 157, 157, 157, 157, 157, 157, 157, 157, 157, 157, 157, 157, 157, 157, 157, 157, 157, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 
            167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 176, 177, 178, 178, 178, 179, 180];
        
        this.pixels[0] = new Array(51, 51);
        this.pixels[1] = new Array(51, 51);
        this.pixels[2] = new Array(51, 51);
        this.pixels[3] = new Array(51, 51);
        this.pixels[4] = new Array(51, 51);
        this.pixels[5] = new Array(51, 51);
        this.pixels[6] = new Array(51, 51);
        this.pixels[7] = new Array(51, 51);
        this.pixels[8] = new Array(51, 51);
        this.pixels[9] = new Array(51, 51);
        this.pixels[10] = new Array(51, 51);
        this.pixels[11] = new Array(51, 51);
        this.pixels[12] = new Array(51, 51);
        this.pixels[13] = new Array(51, 51);
        this.pixels[14] = new Array(49, 52);
        this.pixels[15] = new Array(50, 53);
        this.pixels[16] = new Array(49, 53);
        this.pixels[17] = new Array(48, 54);
        this.pixels[18] = new Array(47, 55);
        this.pixels[19] = new Array(47, 55);
        this.pixels[20] = new Array(47, 55);
        this.pixels[21] = new Array(47, 55);
        this.pixels[22] = new Array(47, 55);
        this.pixels[23] = new Array(47, 55);
        this.pixels[24] = new Array(47, 55);
        this.pixels[25] = new Array(47, 55);
        this.pixels[26] = new Array(47, 55);
        this.pixels[27] = new Array(47, 55);
        this.pixels[28] = new Array(47, 55);
        this.pixels[29] = new Array(46, 56);
        this.pixels[30] = new Array(46, 56);
        this.pixels[31] = new Array(46, 56);
        this.pixels[32] = new Array(46, 56);
        this.pixels[33] = new Array(46, 56);
        this.pixels[34] = new Array(46, 56);
        this.pixels[35] = new Array(46, 56);
        this.pixels[36] = new Array(46, 56);
        this.pixels[37] = new Array(46, 56);
        this.pixels[38] = new Array(46, 56);
        this.pixels[39] = new Array(46, 56);
        this.pixels[40] = new Array(46, 56);
        this.pixels[41] = new Array(46, 56);
        this.pixels[42] = new Array(46, 56);
        this.pixels[43] = new Array(46, 56);
        this.pixels[44] = new Array(46, 56);
        this.pixels[45] = new Array(46, 56);
        this.pixels[46] = new Array(46, 56);
        this.pixels[47] = new Array(46, 56);
        this.pixels[48] = new Array(46, 56);
        this.pixels[49] = new Array(46, 56);
        this.pixels[50] = new Array(46, 56);
        this.pixels[51] = new Array(46, 56);
        this.pixels[52] = new Array(46, 56);
        this.pixels[53] = new Array(46, 56);
        this.pixels[54] = new Array(45, 57);
        this.pixels[55] = new Array(45, 57);
        this.pixels[56] = new Array(44, 58);
        this.pixels[57] = new Array(44, 58);
        this.pixels[58] = new Array(43, 59);
        this.pixels[59] = new Array(43, 59);
        this.pixels[60] = new Array(42, 60);
        this.pixels[61] = new Array(42, 60);
        this.pixels[62] = new Array(42, 60);
        this.pixels[63] = new Array(42, 60);
        this.pixels[64] = new Array(42, 60);
        this.pixels[65] = new Array(42, 60);
        this.pixels[66] = new Array(42, 60);
        this.pixels[67] = new Array(42, 60);
        this.pixels[68] = new Array(42, 60);
        this.pixels[69] = new Array(42, 60);
        this.pixels[70] = new Array(42, 60);
        this.pixels[71] = new Array(42, 60);
        this.pixels[72] = new Array(42, 60);
        this.pixels[73] = new Array(42, 60);
        this.pixels[74] = new Array(42, 60);
        this.pixels[75] = new Array(42, 60);
        this.pixels[76] = new Array(42, 60);
        this.pixels[77] = new Array(41, 61);
        this.pixels[78] = new Array(41, 61);
        this.pixels[79] = new Array(41, 61);
        this.pixels[80] = new Array(40, 62);
        this.pixels[81] = new Array(40, 62);
        this.pixels[82] = new Array(39, 63);
        this.pixels[83] = new Array(38, 64);
        this.pixels[84] = new Array(38, 64);
        this.pixels[85] = new Array(38, 64);
        this.pixels[86] = new Array(38, 64);
        this.pixels[87] = new Array(38, 64);
        this.pixels[88] = new Array(37, 65);
        this.pixels[89] = new Array(36, 66);
        this.pixels[90] = new Array(36, 66);
        this.pixels[91] = new Array(35, 67);
        this.pixels[92] = new Array(35, 67);
        this.pixels[93] = new Array(34, 68);
        this.pixels[94] = new Array(34, 68);
        this.pixels[95] = new Array(33, 69);
        this.pixels[96] = new Array(33, 69);
        this.pixels[97] = new Array(32, 70);
        this.pixels[98] = new Array(31, 71);
        this.pixels[99] = new Array(31, 71);
        this.pixels[100] = new Array(30, 72);
        this.pixels[101] = new Array(30, 72);
        this.pixels[102] = new Array(29, 73);
        this.pixels[103] = new Array(29, 73);
        this.pixels[104] = new Array(28, 74);
        this.pixels[105] = new Array(28, 74);
        this.pixels[106] = new Array(27, 75);
        this.pixels[107] = new Array(26, 76);
        this.pixels[108] = new Array(26, 76);
        this.pixels[109] = new Array(25, 77);
        this.pixels[110] = new Array(25, 77);
        this.pixels[111] = new Array(24, 78);
        this.pixels[112] = new Array(24, 78);
        this.pixels[113] = new Array(23, 79);
        this.pixels[114] = new Array(23, 79);
        this.pixels[115] = new Array(22, 80);
        this.pixels[116] = new Array(21, 81);
        this.pixels[117] = new Array(21, 81);
        this.pixels[118] = new Array(20, 82);
        this.pixels[119] = new Array(20, 82);
        this.pixels[120] = new Array(19, 83);
        this.pixels[121] = new Array(19, 83);
        this.pixels[122] = new Array(18, 84);
        this.pixels[123] = new Array(18, 84);
        this.pixels[124] = new Array(17, 85);
        this.pixels[125] = new Array(17, 85);
        this.pixels[126] = new Array(16, 86);
        this.pixels[127] = new Array(15, 87);
        this.pixels[128] = new Array(14, 88);
        this.pixels[129] = new Array(13, 89);
        this.pixels[130] = new Array(13, 89);
        this.pixels[131] = new Array(13, 89);
        this.pixels[132] = new Array(13, 89);
        this.pixels[133] = new Array(13, 89);
        this.pixels[134] = new Array(12, 90);
        this.pixels[135] = new Array(12, 90);
        this.pixels[136] = new Array(11, 91);
        this.pixels[137] = new Array(10, 92);
        this.pixels[138] = new Array(10, 92);
        this.pixels[139] = new Array(9, 93);
        this.pixels[140] = new Array(9, 93);
        this.pixels[141] = new Array(8, 94);
        this.pixels[142] = new Array(8, 94);
        this.pixels[143] = new Array(7, 95);
        this.pixels[144] = new Array(7, 95);
        this.pixels[145] = new Array(6, 96);
        this.pixels[146] = new Array(5, 97);
        this.pixels[147] = new Array(5, 97);
        this.pixels[148] = new Array(4, 98);
        this.pixels[149] = new Array(4, 98);
        this.pixels[150] = new Array(3, 99);
        this.pixels[151] = new Array(3, 99);
        this.pixels[152] = new Array(2, 100);
        this.pixels[153] = new Array(2, 100);
        this.pixels[154] = new Array(1, 101);
        this.pixels[155] = new Array(1, 101);
        this.pixels[156] = new Array(1, 101);
        this.pixels[157] = new Array(2, 100);
        this.pixels[158] = new Array(3, 99);
        this.pixels[159] = new Array(4, 98);
        this.pixels[160] = new Array(5, 97);
        this.pixels[161] = new Array(6, 96);
        this.pixels[162] = new Array(7, 95);
        this.pixels[163] = new Array(8, 94);
        this.pixels[164] = new Array(9, 93);
        this.pixels[165] = new Array(10, 92);
        this.pixels[166] = new Array(11, 91);
        this.pixels[167] = new Array(12, 90);
        this.pixels[168] = new Array(13, 89);
        this.pixels[169] = new Array(14, 88);
        this.pixels[170] = new Array(15, 87);
        this.pixels[171] = new Array(16, 86);
        this.pixels[172] = new Array(17, 85);
        this.pixels[173] = new Array(18, 84);
        this.pixels[174] = new Array(19, 83);
        this.pixels[175] = new Array(20, 82);
        this.pixels[176] = new Array(21, 81);
        this.pixels[177] = new Array(22, 80);
        this.pixels[178] = new Array(23, 79);
        this.pixels[179] = new Array(24, 78);
        this.pixels[180] = new Array(25, 77);
        this.pixels[181] = new Array(26, 76);
        this.pixels[182] = new Array(27, 75);
        this.pixels[183] = new Array(28, 74);
        this.pixels[184] = new Array(29, 73);
        this.pixels[185] = new Array(30, 72);
        this.pixels[186] = new Array(31, 71);
        this.pixels[187] = new Array(32, 70);
        this.pixels[188] = new Array(33, 69);
        this.pixels[189] = new Array(34, 68);
        this.pixels[190] = new Array(35, 67);
        this.pixels[191] = new Array(36, 66);
        this.pixels[192] = new Array(37, 65);
        this.pixels[193] = new Array(38, 64);
        this.pixels[194] = new Array(39, 63);
        this.pixels[195] = new Array(40, 62);
        this.pixels[196] = new Array(41, 61);
        this.pixels[197] = new Array(42, 60);
        this.pixels[198] = new Array(43, 59);
        this.pixels[199] = new Array(43, 59);
        this.pixels[200] = new Array(43, 59);
        this.pixels[201] = new Array(43, 59);
        this.pixels[202] = new Array(43, 59);
        this.pixels[203] = new Array(43, 59);
        this.pixels[204] = new Array(43, 59);
        this.pixels[205] = new Array(44, 58);
        this.pixels[206] = new Array(44, 58);
        this.pixels[207] = new Array(45, 57);
        this.pixels[208] = new Array(45, 57);
        this.pixels[209] = new Array(45, 57);
        this.pixels[210] = new Array(45, 57);
        this.pixels[211] = new Array(45, 57);
        this.pixels[212] = new Array(46, 56);
        this.pixels[213] = new Array(46, 56);
        this.pixels[214] = new Array(46, 56);
        this.pixels[215] = new Array(46, 56);
        this.pixels[216] = new Array(46, 56);
        this.pixels[217] = new Array(47, 55);
        this.pixels[218] = new Array(48, 54);
        this.pixels[219] = new Array(48, 54);
        this.pixels[220] = new Array(49, 53);
        this.pixels[221] = new Array(50, 52);
        this.pixels[222] = new Array(51);
        this.pixels[223] = new Array(51);
    }
    
    function reverse() {
        return this.pixels.reverse();
    }
    
    function inBoundsTop(fighterOffset, y) {
        if(y - fighterOffset < 0) {
            return false;
        } else {
            return true;
        }
    }

    function inBoundsLeft(fighterOffset, y) {
        if(y - fighterOffset < 0) {
            return false;
        } else {
            return true;
        }
    }

    function inBoundsBottom(fighterOffset, y) {
        if(y + fighterOffset > area.height() - fighter.height) {
            return false;
        } else {
            return true;
        }
    }

    function inBoundsRight(fighterOffset, y) {
        if(y + fighterOffset > area.width() - fighter.width) {
            return false;
        } else {
            return true;
        }
    }

    function up() {
        if(this.inBoundsTop(fighterOffset, this.y)) {
            this.y -= fighterOffset;
            $('.' + this.cls).css('top', this.y);
            return true;
        } else {
            this.clearMirageInterval();
            return false;
        }
    }

    function left() {
        if(this.inBoundsLeft(fighterOffset, this.x)) {
            this.x -= fighterOffset;
            $('.' + this.cls).css('left', this.x);
            return true;
        } else {
            this.clearMirageInterval();
            return false;
        }
    }

    function down() {
        var collision = false;
        
        if(this.isEnemy && collide(this, fighter)) {
            collision = true;
        }
        
        if(this.isEnemy && (this.y == area.height() - this.height || collision)) {
            if(collision) {
                endFighter();
            } else {
                newEnemy();
            }
            
            return false;
        }
        
        
        if(this.inBoundsBottom(fighterOffset, this.y)) {
            this.y += fighterOffset;
            $('.' + this.cls).css('top', this.y);
            return true;
        } else {
            this.clearMirageInterval();
            return false;
        }
    }

    function right() {
        if(this.inBoundsRight(fighterOffset, this.x)) {
            this.x += fighterOffset;
            $('.' + this.cls).css('left', this.x);
            return true;
        } else {
            this.clearMirageInterval();
            return false;
        }
    }

    function clearMirageInterval() {
        if(this.mirageInterval != null) {
            clearInterval(this.mirageInterval);
            this.mirageInterval = null;
        }
    }

    function destroy() {
        $('.' + this.cls).remove();
    }
}

function unlockBullet() {
    lockBullet = false;
}

function endFighter() {
    area.append('<div class="explosion" style="top: ' + fighter.y + 'px; left: ' + fighter.x + 'px;"></div>');
    explosion = true;
    $('.explosion').fadeOut(5000, function() {
        explosion = false;
    });
    enemy.clearMirageInterval();
    enemy.dissappear();
    
    fighter.clearMirageInterval();
    fighter.dissappear();
    
    fighterGameOver = true;
}

function newEnemy() {
    enemy.clearMirageInterval();
    enemy.dissappear();
}

function increaseSpeed() {
    enemySpeed = defaultEnemySpeed - parseInt(fighterScore/1000) * 10;
    
    if(enemySpeed < 0) {
        enemySpeed = 0;
    }
}

$(document).ready(function() {
    var fighterArea = $('.fighter');
    mirageImg = $('.mirage');
    enemyImg = $('.enemy');
    
    area = $('#fighter');
    
    $('#start-fighter', fighterArea).on('click', function() {
        if (fighterGameOver && !explosion) {
            enemySpeed = defaultEnemySpeed;
            fighter = new Mirage(false);
            enemy = new Mirage(true);
            fighterScore = 0;
            $('#fighter-score').html("0");
            fighterGameOver = false;
        }
    });
    
    $('#up-fighter', fighterArea).on('mousedown', function() {
        if (!fighterGameOver) {
            fighter.clearMirageInterval();
            fighter.up();
            fighter.mirageInterval = setInterval('fighter.up()', fighterSpeed);
        }
    });
    
    $('#up-fighter', fighterArea).on('mouseup', function() {
        if (!fighterGameOver) {
            fighter.clearMirageInterval();
        }
    });
    
    $('#left-fighter', fighterArea).on('mousedown', function() {
        if (!fighterGameOver) {
            fighter.clearMirageInterval();
            fighter.left();
            fighter.mirageInterval = setInterval('fighter.left()', fighterSpeed);
        }
    });
    
    $('#left-fighter', fighterArea).on('mouseup', function() {
        if (!fighterGameOver) {
            fighter.clearMirageInterval();
        }
    });
    
    $('#down-fighter', fighterArea).on('mousedown', function() {
        if (!fighterGameOver) {
            fighter.clearMirageInterval();
            fighter.down();
            fighter.mirageInterval = setInterval('fighter.down()', fighterSpeed);
        }
    });
    
    $('#down-fighter', fighterArea).on('mouseup', function() {
        if (!fighterGameOver) {
            fighter.clearMirageInterval();
        }
    });
    
    $('#right-fighter', fighterArea).on('mousedown', function() {
        if (!fighterGameOver) {
            fighter.clearMirageInterval();
            fighter.right();
            fighter.mirageInterval = setInterval('fighter.right()', fighterSpeed);
        }
    });
    
    $('#right-fighter', fighterArea).on('mouseup', function() {
        if (!fighterGameOver) {
            fighter.clearMirageInterval();
        }
    });
    
    $('#fire-fighter', fighterArea).on('click', function() {
        if (!fighterGameOver && !lockBullet) {
            lockBullet = true;
            fighter.fire();
            setTimeout('unlockBullet()', 1000);
        }
    });
});